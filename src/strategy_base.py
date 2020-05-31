# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import enum

class StrategyBase(object):
    def __init__(self, data_source):
        self.__name = "strategy_base"
        self.__data_source = data_source

    def position_must_be_closed(self, order):
        # update data
        # decide based on order
        return

    def get_orders_to_be_opened(self):
        # update data
        # return either an order, if a position has to be openend or None
        return

    def position_must_be_updated(self, order):
        # update data
        # decide if order has to be updated
        return

    def get_name(self):
        return self.__name
