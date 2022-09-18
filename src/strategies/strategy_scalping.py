# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging

from strategy_base import StrategyBase
from trade_objects import Order, Signal

logger = logging.getLogger()


class StrategyScalping(StrategyBase):
    def __init__(self, data_source, symbol, positions_manager=None):
        super().__init__(positions_manager)
        self.name = "strategy_scalping"
        self._datasource = data_source
        self._symbol = symbol

        self._datasource.subscribe_bars(self._symbol)


    def _calc_buy_signal(self, data):
        mavg = data.rolling(21).mean().close.values
        closes = data.close.values

        if closes[-2] < mavg[-2] and closes[-1] > mavg[-1]:
            logger.info(
                f'buy signal: closes[-2] {closes[-2]} < mavg[-2] {mavg[-2]} '
                f'closes[-1] {closes[-1]} > mavg[-1] {mavg[-1]}')
            return True
        else:
            logger.info(
                f'closes[-2:] = {closes[-2:]}, mavg[-2:] = {mavg[-2:]}')
            return False


    def analyse_data(self, data):
        position = None
        positions_for_strategy = self.positions_manager.get_open_positons_for_strategy(self.name)

        for item in positions_for_strategy:
            if self._symbol == item.order.ticker_symbol:
                position = item

        if position is not None:
            current_price = float(self._datasource.get_latest_trade(self._symbol).price)
            cost_basis = float(position.avg_entry_price)
            limit_price = max(cost_basis + 0.01, current_price)

            # TODO: Closing order cannot have timeout time
            order = Order(self._symbol, 'sell', 0.1, 120, price=limit_price)
            logger.info(f'exit position')
            return [Signal(self.name, order, True)]

        elif not self.positions_manager.ticker_is_busy(self._symbol):
            signal = self._calc_buy_signal(data)
            if signal:
                price = self._datasource.get_latest_trade(self._symbol).price
                order = Order(self._symbol, 'buy', 0.1, 120, price=price)

                return [Signal(self.name, order, False)]

        else:
            return []


    async def get_trade_signals(self):
        data = await self._datasource.get_latest_bars(self._symbol)

        if data is not None and len(data) > 20:
            result = self.analyse_data(data)
            return result
        else:
            return []
