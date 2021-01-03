# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategies.strategy_a import StrategyA
from data_sources.t212_data_source import T212DataSource as T212

class StrategiesManager(object):
    def __init__(self, session_manager):
        self.__session_manager = session_manager
        self.__strategies = self.__select_strategies()

    def __select_strategies(self):
        # It could be a dictionary {"strategy_name" : strategy instance}
        strategies = {"strategy_a": StrategyA(T212(self.__session_manager))}
        # select strategies, instantiate one for each with the
        # data source and add them to strategies
        return strategies

    def get_strategy(self, strategy_name):
        return self.__strategies[strategy_name]

    def get_strategies(self):
        return self.__strategies
