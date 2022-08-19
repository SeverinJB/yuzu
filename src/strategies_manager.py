# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategies.strategy_scalping import StrategyScalping
from data_sources.alpaca_data_source import AlpacaDataSource

import asyncio
import sys
import logging

logger = logging.getLogger()

class StrategiesManager(object):
    def __init__(self, session_manager):
        self.__session_manager = session_manager
        self.__strategies = self.__select_strategies()

    def __select_strategies(self):
        # It could be a dictionary {"strategy_name" : strategy instance}
        #strategies = {"strategy_scalping": StrategyScalping(AlpacaDataSource(
        #    self.__session_manager)}

        logger.info(f'Strategies Manager initiating strategies')

        strategies = {"strategy_scalping": StrategyScalping(AlpacaDataSource(
            self.__session_manager), 'AAPL', 2000, self.__session_manager)}

        # select strategies, instantiate one for each with the
        # data source and add them to strategies
        return strategies

    def get_strategy(self, strategy_name):
        return self.__strategies[strategy_name]

    def get_strategies(self):
        return self.__strategies
