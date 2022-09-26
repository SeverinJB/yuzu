# Copyright Yuzu Trading 2022
# Any unauthorised usage forbidden

import logging

from strategy_base import StrategyBase
from trade_objects import Order, Signal

logger = logging.getLogger()


class StrategyScalping(StrategyBase):
    def __init__(self, broker, ticker):
        super().__init__(broker.positions_manager)
        self.name = "strategy_scalping"
        self.broker = broker.name
        self.__datasource = broker.data_source
        self.__ticker = ticker

        self.__datasource.subscribe_bars(self.__ticker)


    def get_open_positions(self):
        return self.positions_manager.get_open_positions_for_strategy(self.name)


    def get_name(self):
        return self.name


    def __calc_buy_signal(self, data):
        mavg = data.rolling(11).mean().close.values
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


    def __get_signal(self, data):
        position = None
        positions_for_strategy = self.get_open_positions()

        for position in positions_for_strategy:
            if self.__ticker == position.ticker:
                if not self.positions_manager.pending_order_exists_for_ticker(self.__ticker):
                    position = position

        if position is not None:
            current_price = float(self.__datasource.get_latest_trade(self.__ticker).price)
            cost_basis = float(position.avg_entry_price)
            limit_price = max(cost_basis + 0.01, current_price)

            # FIXME: Closing order cannot have timeout time
            order = Order(self.name, self.broker, self.__ticker, 'sell', 0.1, 120,
                          price=limit_price)
            logger.info(f'exit position')
            return [Signal(order, True)]

        elif not self.positions_manager.ticker_is_busy(self.__ticker) and data is not None:
            if len(data) > 10:
                signal = self.__calc_buy_signal(data)
                if signal:
                    price = self.__datasource.get_latest_trade(self.__ticker).price
                    order = Order(self.name, self.broker, self.__ticker, 'buy', 0.1, 120,
                                  price=price)

                    return [Signal(order, False)]


    async def get_trade_signals(self):
        data = await self.__datasource.get_latest_bars(self.__ticker)
        signal = self.__get_signal(data)
        return signal
