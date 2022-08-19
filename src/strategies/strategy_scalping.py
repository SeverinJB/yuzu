# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pandas as pd
import pytz
import logging
import asyncio
import sys

logger = logging.getLogger()

from strategy_base import StrategyBase
from trade_objects import Side, Order, Signal

class StrategyScalping(StrategyBase):
    def __init__(self, data_source, symbol, lot, api):
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
                data = data_source.get_data(symbol, start, end)
                break
            except:
                # make sure we get bars
                pass
        bars = data[market_open:]
        self._bars = bars

        self._init_state()


    def _init_state(self):
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


    def _outofmarket(self):
        return self._now().time() >= pd.Timestamp('15:55').time()


    def checkup(self, position):
        # self._l.info('periodic task')

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

        #if self._position is not None and self._outofmarket():
        #    self._submit_sell(bailout=True)


    def _cancel_order(self):
        if self._order is not None:
            self._api.cancel_order(self._order.id)


    def _calc_buy_signal(self):
        mavg = self._bars.rolling(3).mean().close.values
        closes = self._bars.close.values
        if closes[-2] < mavg[-2] and closes[-1] > mavg[-1]:
            self._l.info(
                f'buy signal: closes[-2] {closes[-2]} < mavg[-2] {mavg[-2]} '
                f'closes[-1] {closes[-1]} > mavg[-1] {mavg[-1]}')
            return True
        else:
            self._l.info(
                f'closes[-2:] = {closes[-2:]}, mavg[-2:] = {mavg[-2:]}')
            return False


    def on_bar(self, bar):
        self._bars = self._bars.append(pd.DataFrame({
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume,
        }, index=[pd.Timestamp(bar.timestamp, tz=pytz.UTC)]))

        self._l.info(
            f'received bar start: {pd.Timestamp(bar.timestamp)}, close: {bar.close}, len(bars): {len(self._bars)}')
        if len(self._bars) < 4:
            return
        if self._outofmarket():
            return
        if self._state == 'TO_BUY':
            signal = self._calc_buy_signal()
            if signal:
                trade = self._api.get_latest_trade(self._symbol)
                order = Order(self._symbol, Side.SELL, 0.1, price=trade)

                return [Signal(order, False)]


    async def get_trade_signals(self):
        result = None

        if result is None:
            return []
        else:
            return result
