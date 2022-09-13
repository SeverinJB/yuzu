# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import pandas as pd
import pytz
import logging

logger = logging.getLogger()

from strategy_base import StrategyBase
from trade_objects import Side, Order, Signal

class StrategyScalping(StrategyBase):
    def __init__(self, data_source, symbol, lot, api, positions_manager=None):
        super().__init__(positions_manager)
        self._api = api.get_session()
        self._stream = api.get_stream()
        self._symbol = symbol
        self._lot = lot
        self._bars = []
        self._l = logger.getChild(self._symbol)
        self._datasource = data_source

        self._datasource.subscribe_bars(self._symbol)

        now = pd.Timestamp.now(tz='America/New_York').floor('1min')
        market_open = now.replace(hour=9, minute=30)
        start = (now - pd.Timedelta('1day')).strftime('%Y-%m-%dT%H:%M:%SZ')
        end = (now).strftime('%Y-%m-%dT%H:%M:%SZ')
        tomorrow = (now + pd.Timedelta('1day')).strftime('%Y-%m-%d')
        while 1:
            # at inception this results sometimes in api errors. this will work
            # around it. feel free to remove it once everything is stable
            try:
                logger.info(f'Receiving historic data')
                data = data_source.get_data(symbol, start, end)
                logger.info(f'Historic data received')
                break
            except:
                # make sure we get bars
                pass
        bars = data[market_open:]
        self._bars = bars

        self._init_state()


    def _init_state(self):
        # TODO: Should be handled by position_manager(?)

        symbol = self._symbol
        order = [o for o in self._api.list_orders() if o.symbol == symbol]
        position = [p for p in self._api.list_positions()
                    if p.symbol == symbol]
        self._order = order[0] if len(order) > 0 else None
        self._position = position[0] if len(position) > 0 else None
        if self._position is not None:
            if self._order is None:
                self._state = 'TO_SELL'
            else:
                self._state = 'SELL_SUBMITTED'
                if self._order.side != 'sell':
                    self._l.warn(
                        f'state {self._state} mismatch order {self._order}')
        else:
            if self._order is None:
                self._state = 'TO_BUY'
            else:
                self._state = 'BUY_SUBMITTED'
                if self._order.side != 'buy':
                    self._l.warn(
                        f'state {self._state} mismatch order {self._order}')

    def _now(self):
        return pd.Timestamp.now(tz='America/New_York')


    def checkup(self, position):
        # TODO: Should be handled by trade_manager

        now = self._now()
        order = self._order
        if (order is not None and
            order.side == 'buy' and now -
                order.submitted_at.tz_convert(tz='America/New_York') > pd.Timedelta('2 min')):
            last_price = self._api.get_latest_trade(self._symbol).price
            self._l.info(
                f'canceling missed buy order {order.id} at {order.limit_price} '
                f'(current price = {last_price})')
            self._cancel_order()


    def _cancel_order(self):
        # TODO: Should be handled by either trade_manager or position_manager

        if self._order is not None:
            self._api.cancel_order(self._order.id)


    def _calc_buy_signal(self):
        mavg = self._bars.rolling(21).mean().close.values
        closes = self._bars.close.values

        #if closes[-2] < mavg[-2] and closes[-1] > mavg[-1]:
        if True:
            self._l.info(
                f'buy signal: closes[-2] {closes[-2]} < mavg[-2] {mavg[-2]} '
                f'closes[-1] {closes[-1]} > mavg[-1] {mavg[-1]}')
            return True
        else:
            self._l.info(
                f'closes[-2:] = {closes[-2:]}, mavg[-2:] = {mavg[-2:]}')
            return False


    def on_bar(self, data):
        # TODO: Should data_sources objects handle data entirely?

        new_bar = False

        for bar in data:
            if (len(self._bars.index.values) > 0) and (pd.Timestamp(bar["timestamp"]) <= \
                    self._bars.index.values[-1]):
                pass
            else:
                self._bars = self._bars.append(pd.DataFrame({
                    'open': float(bar["open"]),
                    'high': float(bar["high"]),
                    'low': float(bar["low"]),
                    'close': float(bar["close"]),
                    'volume': float(bar["volume"]),
                }, index=[pd.Timestamp(bar["timestamp"], tz=pytz.UTC)]))
                self._l.info(
                    f'received bar start: {pd.Timestamp(bar["timestamp"])}, close: {bar["close"]}, len(bars): {len(self._bars)}')

                new_bar = True

        if len(self._bars) < 20:
            return

        if self.positions_manager.ticker_is_busy(self._symbol):
            current_price = float(self._api.get_latest_trade(self._symbol))
            cost_basis = float(self._position.avg_entry_price)
            limit_price = max(cost_basis + 0.01, current_price)
            order = Order(self._symbol, Side.SELL, 0.1, price=limit_price)
            self._l.info(f'exit position')
            return [Signal(order, False)]

        elif new_bar and not self.positions_manager.ticker_is_busy(self._symbol):
            signal = self._calc_buy_signal()
            if signal:
                trade = self._api.get_latest_trade(self._symbol)
                order = Order(self._symbol, Side.SELL, 0.1, price=trade)

                return [Signal(order, False)]


    async def get_trade_signals(self):
        result = self.on_bar(self._datasource.get_latest_bars())

        if result is None:
            return []
        else:
            return result
