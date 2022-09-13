# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging
import pandas as pd
import asyncio

from trade_objects import Position

logger = logging.getLogger()

class TradeManager(object):
    def __init__(self, trade_executor, strategies_manager, positions_manager):
        self.__executor = trade_executor
        self.__strategies_manager = strategies_manager
        self.__positions_manager = positions_manager


    def _outofmarket(self):
        opening_time = pd.Timestamp('09:30').time()
        now = pd.Timestamp.now(tz='America/New_York').floor('1min').time()
        closure_time = pd.Timestamp('16:00').time()

        market_closed = (opening_time >= now) or (closure_time <= now)

        return market_closed


    async def trade(self):
        if self._outofmarket():
            logger.info(f'Out of market')
            await asyncio.sleep(60)
            # TODO: Implement bailout before market closure
            # if self._position is not None and self._outofmarket():
            #    self._submit_sell(bailout=True)

        else:
            #self.__positions_manager.update_positions()

            exit_orders, entry_orders = await self.__classify_signals(await
                                                                       self.__collect_trade_signals())
            await self.__exit_positions(exit_orders)
            await self.__enter_positions(entry_orders)


    async def __collect_trade_signals(self):
        signals = []
        for strategy in self.__strategies_manager.get_strategies().values():
            signals.extend(await strategy.get_trade_signals())

        return signals


    async def __classify_signals(self, signals):
        exit_orders = []
        entry_orders = []

        for signal in signals:
            if signal.exits_position:
                exit_orders.append(signal.order)
            else:
                entry_orders.append(signal.order)

        return exit_orders, entry_orders


    async def __exit_positions(self, exit_orders):
        for order in exit_orders:
            order_response = await self.__executor.submit_order(order)
            if order_response is not None:
                closed_size = order_response.order.size
                if closed_size == self.__positions_manager.get_open_position(
                        order.ticker_symbol).size:
                    self.__positions_manager.close_position(order.ticker_symbol)
                else:
                    # TODO: Implement and test this method
                    self.__positions_manager.update_position(order.ticker_symbol, closed_size)
            else:
                # TODO: Decide what to do if position cannot be opened
                raise Exception("TradeManager: failed to exit position!")


    async def __enter_positions(self, entry_orders):
        for order in entry_orders:
            ticker = order.ticker_symbol
            if self.__positions_manager.ticker_is_busy(ticker):
                raise Exception("PositionsManager: Trying to open position for busy ticker!")
            else:
                order_response = await self.__executor.submit_order(order)

            if order_response is not None:
                self.__positions_manager.open_position(Position(order=order))
            else:
                # TODO: Decide what to do if position cannot be opened
                # raise Exception("TradeManager: failed to enter position!")
                pass
