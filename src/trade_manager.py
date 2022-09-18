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


    def __now(self):
        return pd.Timestamp.now(tz='America/New_York')


    def __outofmarket(self):
        opening_time = pd.Timestamp('09:30').time()
        now = self.__now().floor('1min').time()
        closure_time = pd.Timestamp('16:00').time()

        market_closed = (opening_time >= now) or (closure_time <= now)

        return market_closed


    async def __exit_positions(self, exit_orders):
        for order in exit_orders:
            order_response = await self.__executor.submit_order(order)
            if order_response is not None:
                self.__positions_manager.close_position(order.ticker_symbol)

            # if order_response is not None:
            #     closed_size = order_response.order.size
            #     if closed_size == self.__positions_manager.get_open_position(
            #             order.ticker_symbol).size:
            #         self.__positions_manager.close_position(order.ticker_symbol)
            #     else:
            #         # TODO: Implement and test this method
            #         self.__positions_manager.update_position(order.ticker_symbol, closed_size)
            # else:
            #     # TODO: Decide what to do if position cannot be opened
            #     raise Exception("TradeManager: failed to exit position!")


    async def __enter_positions(self, entry_orders):
        for order in entry_orders:
            ticker = order.ticker_symbol
            if self.__positions_manager.ticker_is_busy(ticker):
                raise Exception("PositionsManager: Trying to open position for busy ticker!")
            else:
                self.__positions_manager.add_pending_order(Position(order=order))
                order_response = await self.__executor.submit_order(order)

            # TODO: Implement update function that switches from pending to fulfilled
            # if order_response is not None:
            #     self.__positions_manager.open_position(Position(order=order))
            # else:
            #     # TODO: Decide what to do if position cannot be opened
            #     # raise Exception("TradeManager: failed to enter position!")
            #     pass


    async def __classify_signals(self, signals):
        exit_orders = []
        entry_orders = []

        for signal in signals:
            if signal.exits_position:
                exit_orders.append(signal.order)
            else:
                entry_orders.append(signal.order)

        return exit_orders, entry_orders


    async def __collect_trade_signals(self):
        signals = []
        for strategy in self.__strategies_manager.get_strategies().values():
            signals.extend(await strategy.get_trade_signals())

        return signals


    async def __check_for_updates(self):
        raise NotImplementedError


    async def __time_out_pending_orders(self):
        now = self.__now()
        for position in self.__positions_manager.get_pending_orders().values():
            if (now - position.order.submitted_at.tz_convert(tz='America/New_York')
                    > pd.Timedelta(position.order.valid_for_seconds, "seconds")):
                self.__executor.cancel_order(position.order.id)
                self.__positions_manager.delete_pending_order(position.order.ticker_symbol)
        await asyncio.sleep(30)


    async def trade(self):
        if self.__outofmarket():
            logger.info(f'Out of market')
            await asyncio.sleep(60)
            # TODO: Implement bailout before market closure
            # if self._position is not None and self._outofmarket():
            #    self._submit_sell(bailout=True)

        else:
            # await self.__check_for_updates()
            # await self.__time_out_pending_orders()

            trade_signals = await self.__collect_trade_signals()
            exit_orders, entry_orders = await self.__classify_signals(trade_signals)

            await self.__exit_positions(exit_orders)
            await self.__enter_positions(entry_orders)
