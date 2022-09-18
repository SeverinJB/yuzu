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
        self.__datasource = data_source
        self.__symbol = symbol

        self.__datasource.subscribe_bars(self.__symbol)


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


    def get_signal(self, data):
        position = None
        positions_for_strategy = self.positions_manager.get_open_positons_for_strategy(self.name)

        for item in positions_for_strategy:
            if self.__symbol == item.order.ticker_symbol:
                position = item

        if position is not None:
            current_price = float(self.__datasource.get_latest_trade(self.__symbol).price)
            cost_basis = float(position.avg_entry_price)
            limit_price = max(cost_basis + 0.01, current_price)

            # TODO: Closing order cannot have timeout time
            order = Order(self.__symbol, 'sell', 0.1, 120, price=limit_price)
            logger.info(f'exit position')
            return [Signal(self.name, order, True)]

        elif not self.positions_manager.ticker_is_busy(self.__symbol) and data is not None:
            signal = self._calc_buy_signal(data)
            if signal:
                price = self.__datasource.get_latest_trade(self.__symbol).price
                order = Order(self.__symbol, 'buy', 0.1, 120, price=price)

                return [Signal(self.name, order, False)]

        else:
            return []


    async def get_trade_signals(self):
        data = await self.__datasource.get_latest_bars(self.__symbol)
        signal = self.get_signal(data)
        return signal
