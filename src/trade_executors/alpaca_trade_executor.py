# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from trade_executor_base import TradeExecutorBase


class AlpacaTradeExecutor(TradeExecutorBase):
    def __init__(self, session_manager):
        super().__init__()
        self.__session_manager = session_manager

    def __send_request(self):
        raise NotImplementedError

    def submit_order(self, order):
        self.__session_manager.get_session().submit_order(
            symbol='SPY',
            side='buy',
            type='market',
            qty=1,
            time_in_force='day',
        )

    def cancel_order(self, order_id):
        raise NotImplementedError

    def cancel_all_orders(self):
        raise NotImplementedError
