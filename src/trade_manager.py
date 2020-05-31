# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import enum

class Position(object):
    def __init__(self, strategy_name, order, id):
        self.strategy = strategy_name
        self.order = order
        self.trade_id = id

class TradeManager(object):
    def __init__(self, trade_executor, strategy_manager):
        self.__executor = trade_executor
        self.__strategy_manager = strategy_manager
        self.opened_positions = {}
        self.pending_orders = {}

    def __update_orders(self):
        # TODO: Find a way to check if some pending orders have been executed a
        # nd/or if stop loss/tp has been triggered
        return

    def __close_positions(self):
        for position in self.opened_positions:
            strategy = self.__strategy_manager.get_strategy(position.strategy)
            if strategy.position_must_be_closed(position.order):
                self.__executor.close_position(position.id)
                del self.opened_positions[position.order.ticker_symbol]

    def __open_positions(self):
        for strategy in self.__strategy_manager.get_strategies():
            orders_to_open = strategy.get_orders_to_be_opened()
            for order in orders_to_open:
                ticker = order.ticker_symbol
                if not ticker in self.opened_positions and not ticker in self.pending_orders:
                    order_id = self.__executor.submit_order(order)
                    self.opened_positions[ticker] = Position(strategy.get_name(), order, order_id)
                    # TODO add it to pending orders instead if not market order

    def trade(self):
        self.__update_orders()
        self.__close_positions()
        self.__open_positions()
        # TODO: Add possibility of closing only part of position
