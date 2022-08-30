# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

from trade_objects import Position

class PositionsManager(object):
    def __init__(self):
        self.__open_positions = {} # ticker as key
        self.__pending_orders = {} # ticker as key

    def update_positions(self, broker):
        # TODO: Implement to update pending orders and postitions with triggered sl/tp
        pass

    def open_position_exists_for_ticker(self, ticker):
        return ticker in self.__open_positions

    def pending_order_exists_for_ticker(self, ticker):
        return ticker in self.__pending_orders

    def ticker_is_busy(self, ticker):
         return self.open_position_exists_for_ticker(ticker) or \
                self.pending_order_exists_for_ticker(ticker)

    def get_open_positons_for_strategy(self, strategy_name):
        positions = []
        for position in self.__open_positions.values():
            if position.strategy == strategy_name:
                positions.append(position)

        return positions

    def get_open_position(self, ticker):
        return self.__open_positions[ticker]

    def get_pending_order(self, ticker):
        return self.__pending_orders[ticker]

    def open_position(self, position):
        ticker = position.order.ticker_symbol
        if self.ticker_is_busy(ticker):
            raise Exception("PositionsManager: Trying to open position for already busy ticker!")

        self.__open_positions[ticker] = position

    def close_position(self, ticker):
        if ticker in self.__open_positions:
            del self.__open_positions[ticker]
        else:
            raise Exception("PositionsManager: Trying to close not existing position!")

    # TODO: Implement opening and canceling of pending orders
