# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

class StrategyBase(object):
    def __init__(self, data_source, positions_manager):
        self.__name = "strategy_base"
        self.__data_source = data_source
        self.__positions_manager = positions_manager

    def get_exit_signals(self):
        # returns a (possibly empty) list of exit signals, in forms of ticker
        return

    def get_entry_signals(self):
        # return a (possibly empty) list of entry signals in forms of orders to execute
        return

    def get_name(self):
        return self.__name
