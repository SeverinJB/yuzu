# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import logging

from strategies.strategy_scalping import StrategyScalping
from data_sources.alpaca_data_source import AlpacaDataSource

logger = logging.getLogger()


class StrategiesManager(object):
    def __init__(self, session_manager, positions_manager):
        self.__session_manager = session_manager
        self.__positions_manager = positions_manager
        self.__strategies = self.__select_strategies()  # {'STRATEGY_NAME' : STRATEGY, ...}


    def __select_strategies(self):
        logger.info(f'Strategies Manager initiating strategies')

        strategies = {
            "strategy_scalping": StrategyScalping(AlpacaDataSource(
                self.__session_manager), 'AAPL', self.__positions_manager),
        }

        return strategies


    def get_strategy(self, strategy_name):
        return self.__strategies[strategy_name]


    def get_strategies(self):
        return self.__strategies
