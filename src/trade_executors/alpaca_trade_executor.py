# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging

from trade_executor_base import TradeExecutorBase

logger = logging.getLogger()


class AlpacaTradeExecutor(TradeExecutorBase):
    def __init__(self, session_manager):
        super().__init__()
        self._session = session_manager.get_session()


    def __send_request(self):
        raise NotImplementedError


    def list_orders(self):
        return self._session.list_orders()


    async def submit_order(self, order):
        amount = int(1000 / order.price)

        try:
            response = await self._session.submit_order(
                symbol=order.ticker_symbol,
                side=order.side,
                type='limit',
                qty=amount,
                time_in_force='day',
                limit_price=order.price,
            )
            logger.info(f'submitted order {order.ticker_symbol}')
            return response

        except Exception as e:
            logger.info(e)
            return


    def cancel_order(self, order):
        return self._session.cancel_order(order.id)


    def cancel_all_orders(self):
        raise NotImplementedError
