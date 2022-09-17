# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging

from strategy_base import StrategyBase
from trade_objects import Side, Order, Signal

logger = logging.getLogger()


class StrategyScalping(StrategyBase):
    def __init__(self, data_source, symbol, lot, api, positions_manager=None):
        super().__init__(positions_manager)
        self.name = "strategy_scalping"

        self._symbol = symbol
        self._l = logger.getChild(self._symbol)
        self._datasource = data_source
        self._position = []

        self._datasource.subscribe_bars(self._symbol)


    def _calc_buy_signal(self, data):
        mavg = data.rolling(21).mean().close.values
        closes = data.close.values

        if closes[-2] < mavg[-2] and closes[-1] > mavg[-1]:
            self._l.info(
                f'buy signal: closes[-2] {closes[-2]} < mavg[-2] {mavg[-2]} '
                f'closes[-1] {closes[-1]} > mavg[-1] {mavg[-1]}')
            return True
        else:
            self._l.info(
                f'closes[-2:] = {closes[-2:]}, mavg[-2:] = {mavg[-2:]}')
            return False


    def analyse_data(self, data):
        if len(data) < 20:
            return None

        # TODO - Fix error: Too many requests for list_positions
        position = []  # [p for p in self._datasource.list_positions() if p.symbol == self._symbol]
        self._position = position[0] if len(position) > 0 else None

        if self._position is not None and self.positions_manager.ticker_is_busy(self._symbol):
            current_price = float(self._datasource.get_latest_trade(self._symbol).price)
            cost_basis = float(self._position.avg_entry_price)
            limit_price = max(cost_basis + 0.01, current_price)

            # TODO: Closing order cannot have timeout time
            order = Order(self._symbol, 'sell', 0.1, 120, price=limit_price)
            self._l.info(f'exit position')
            return [Signal(self.name, order, True)]

        elif not self.positions_manager.ticker_is_busy(self._symbol):
            signal = self._calc_buy_signal(data)
            if signal:
                price = self._datasource.get_latest_trade(self._symbol).price
                order = Order(self._symbol, 'buy', 0.1, 120, price=price)

                return [Signal(self.name, order, False)]


    async def get_trade_signals(self):
        data = await self._datasource.get_latest_bars(self._symbol)
        result = self.analyse_data(data)

        if result is None:
            return []
        else:
            return result
