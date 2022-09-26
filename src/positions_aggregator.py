# Copyright Yuzu Trading 2022
# Any unauthorised usage forbidden

import logging

logger = logging.getLogger()


class PositionsAggregator(object):
    def __init__(self, brokers_manager):
        self.__brokers = brokers_manager.get_brokers()


    def get_pending_orders(self):
        pending_orders = []

        for broker in self.__brokers:
            for order in broker.get_pending_orders().values():
                pending_orders.append(order)

        return pending_orders
