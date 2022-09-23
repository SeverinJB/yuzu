# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging

from trade_executor_base import TradeExecutorBase

logger = logging.getLogger()


class AlpacaTradeExecutor(TradeExecutorBase):
    def __init__(self, session_manager):
        super().__init__(session_manager)
        self.__session = session_manager.get_session()
        self.__trade_updates = {}  # Key is ticker. Value is list of updates.

        self.__subscribe_trade_updates()


    def __send_request(self):
        raise NotImplementedError


    def list_orders(self):
        return self.__session.list_orders()


    def list_positions(self):
        return self.__session.list_positions()


    async def submit_order(self, order):
        if order.price > 1:  # Fixes #21
            order.price = round(order.price, 2)

        amount = int(1000 / order.price)

        try:
            response = self.__session.submit_order(
                symbol=order.ticker,
                side=order.side,
                type='limit',
                qty=amount,
                time_in_force='day',
                limit_price=order.price,
            )
            logger.info(f'submitted order {order.ticker}')
            return response

        except Exception as e:
            logger.info(e)
            return


    async def cancel_order(self, order):
        # FIXME: Returns 200 if cancelling successful, error if not.
        return self.__session.cancel_order(order.id)


    def cancel_all_orders(self):
        raise NotImplementedError


    def __subscribe_trade_updates(self):
        async def on_trade_updates(data):
            logger.info(f'trade_updates {data}')
            ticker = data.order['symbol']

            if ticker not in self.__trade_updates.keys():
                self.__trade_updates[ticker] = []

            self.__trade_updates[ticker].append({'event': data.event, 'order': data.order})

        self.session_manager.get_stream().subscribe_trade_updates(on_trade_updates)


    def get_latest_order_updates(self, ticker):
        if ticker in self.__trade_updates.keys():
            updates = self.__trade_updates[ticker]
            del self.__trade_updates[ticker]
            return updates
        else:
            return None
