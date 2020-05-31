# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

class StrategyBase(object):
    def __init__(self, strategy_name, total_funds):
        self.__name = strategy_name
        self.__total_funds = total_funds
        self.__

    def openNewTrade(self, data, free_funds, open_trades):
        #doSmthg()
        return 0

    def tradeMustBeClosed(self, trade, data):
        return True



