# Copyright Yuzu 2022
# Any unauthorised usage forbidden

import logging

from strategies.strategy_scalping import StrategyScalping

logger = logging.getLogger()


class StrategiesManager(object):
    def __init__(self, brokers_manager):
        self.__brokers = brokers_manager.get_brokers()
        self.__strategies = self.__select_strategies()  # {'STRATEGY_NAME' : STRATEGY, ...}


    def __select_strategies(self):
        logger.info(f'Strategies Manager initiating strategies')

        strategies = {
            'strategy_scalping': StrategyScalping(self.__brokers['alpaca'], 'AAPL'),
            # 'STRATEGY_NAME' : STRATEGY,
        }

        return strategies


    def get_strategy(self, strategy_name):
        return self.__strategies[strategy_name]


    def get_strategies(self):
        return self.__strategies
