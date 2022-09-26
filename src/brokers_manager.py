# Copyright Yuzu Trading 2022
# Any unauthorised usage forbidden

import logging

from broker import Broker

logger = logging.getLogger()


class BrokersManager(object):
    def __init__(self):
        self.name = 'brokers_manager'
        self.__brokers = {}

    def add_broker(self, name, session, trade_executor, data_source, positions_manager,
                   credentials):

        self.__brokers[name] = Broker(name)
        self.__brokers[name].session = session()
        self.__brokers[name].session.login(credentials)
        self.__brokers[name].positions_manager = positions_manager
        self.__brokers[name].data_source = data_source(self.__brokers[name].session)
        self.__brokers[name].trade_executor = trade_executor(self.__brokers[name].session,
                                                             self.__brokers[name].positions_manager)

    def get_brokers(self):
        return self.__brokers
