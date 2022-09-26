# Copyright Yuzu Trading 2022
# Any unauthorised usage forbidden

import logging
import pandas as pd
import asyncio

logger = logging.getLogger()


class TradesManager(object):
    def __init__(self, brokers_manager, strategies_manager, positions_aggregator):
        self.__brokers = brokers_manager.get_brokers()
        self.__strategies_manager = strategies_manager
        self.__positions_aggregator = positions_aggregator


    def __now(self):
        return pd.Timestamp.now(tz='America/New_York')


    def __outofmarket(self):
        today = self.__now()
        opening_time = pd.Timestamp('09:30').time()
        now = today.floor('1min').time()
        closure_time = pd.Timestamp('16:00').time()

        if (opening_time >= now) or (closure_time <= now) or today.weekday() >= 5:
            market_closed = True
        else:
            market_closed = False

        return market_closed


    async def __exit_positions(self, exit_orders):
        for order in exit_orders:
            broker = self.__brokers[order.broker]
            order.submitted_at = self.__now()
            order_response = await broker.trade_executor.submit_order(order)
            return order_response

            # if order_response is not None:
            #     closed_size = order_response.order.size
            #     if closed_size == self.__positions_manager.get_open_position(
            #             order.ticker).size:
            #         self.__positions_manager.close_position(order.ticker)
            #     else:
            #         # TODO: Implement and test this method
            #         self.__positions_manager.update_position(order.ticker, closed_size)
            # else:
            #     # TODO: Decide what to do if position cannot be opened
            #     raise Exception("TradeManager: failed to exit position!")


    async def __enter_positions(self, entry_orders):
        for order in entry_orders:
            ticker = order.ticker
            broker = self.__brokers[order.broker]
            if broker.positions_manager.ticker_is_busy(ticker):
                raise Exception("PositionsManager: Trying to open position for busy ticker!")
            else:
                order.submitted_at = self.__now()
                order_response = await broker.trade_executor.submit_order(order)
                return order_response


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
            signal = await strategy.get_trade_signals()
            if signal is not None:
                signals.extend(signal)

        return signals


    async def __time_out_pending_orders(self):
        # FIXME:    Ensure that cancel_order response is 200 or error
        #           Cancelling orders is important and needs to be done before a ticker is freed.
        now = self.__now()
        for order in self.__positions_aggregator.get_pending_orders():
            submitted_at = order.submitted_at.tz_convert(tz='America/New_York')
            duration_valid = pd.Timedelta(order.valid_for_seconds, "seconds")

            if now - submitted_at > duration_valid:
                broker = self.__brokers[order.broker]
                broker.positions_manager.delete_order(order.ticker)
                response = await broker.trade_executor.cancel_order(order.broker_order_id)

                if response != 200:
                    broker.positions_manager.add_order(order)
                    raise Exception(f'TradesManager: Order was not cancelled correctly, {response}')

            else:
                return None


    async def trade(self):
        if self.__outofmarket():
            logger.info(f'Out of market')
            await asyncio.sleep(60)
            # TODO: Implement bailout before market closure
            # if self._position is not None and self._outofmarket():
            #    self._submit_sell(bailout=True)

        else:
            # await self.__time_out_pending_orders()

            trade_signals = await self.__collect_trade_signals()
            exit_orders, entry_orders = await self.__classify_signals(trade_signals)

            await self.__exit_positions(exit_orders)
            await self.__enter_positions(entry_orders)
