# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from positions_manager import Position
from trade_executor_base import Order

# TODO: Add possibility of closing only part of position

class TradeManager(object):
    def __init__(self, trade_executor, strategy_manager, positions_manager):
        self.__executor = trade_executor
        self.__strategy_manager = strategy_manager
        self.__positions_manager = positions_manager

    def __close_positions(self):
        for strategy in self.__strategy_manager.get_strategies():
            for ticker in strategy.get_exit_signals():
                if self.__positions_manager.open_position_exists_for_ticker(ticker):
                    trade_id = self.__positions_manager.get_open_position(ticker).trade_id
                    if self.__executor.close_position(trade_id):
                        self.__positions_manager.close_position(ticker)
                    else:
                        # TODO: Decide what to do if position cannot be closed
                        raise Exception("TradeManager: failed to close position")

    def __open_positions(self):
        for strategy in self.__strategy_manager.get_strategies():
            for order in strategy.get_entry_signals():
                ticker = order.ticker_symbol
                if not self.__positions_manager.ticker_is_busy(ticker):
                    # TODO: adapt to return type of submit_order()
                    order_response = self.__executor.submit_order(order)
                    if order_response is not None:
                        # TODO: distinguish between open positions and pending orders
                        self.__positions_manager.open_position(
                            Position(strategy.get_name(), order_response.order, order_response.id))
                    else:
                        # TODO: Decide what to do if position cannot be opened
                        raise Exception("TradeManager: failed to open position")

    def trade(self):
        self.__positions_manager.update_positions()
        self.__close_positions()
        self.__open_positions()
