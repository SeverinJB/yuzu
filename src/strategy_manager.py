# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategies import *

class StrategyManager:
    def __init__(self, data_source):
        self.__strategies = self.__select_strategies(data_source)

    def __select_strategies(self, data_source):
        # It could be a dictionary {"strategy_name" : strategy instance}
        strategies = {}
        # select strategies, instantiate one for each with the
        # data source and add them to strategies
        return strategies

    def get_strategy(self, strategy_name):
        return self.__strategies[strategy_name]

    def get_strategies(self):
        return self.__strategies
