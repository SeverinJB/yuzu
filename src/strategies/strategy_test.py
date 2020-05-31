# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategy_base import StrategyBase

class StrategyTest(StrategyBase):
    def __init__(self, data_analyzer, positions_manager=None):
        super().__init__(data_analyzer, positions_manager)
        self.name = "strategy_test"

    def get_entry_signals(self):
        if self.data_analyzer.get_latest_close() > self.data_analyzer.get_latest_sma():
            # define order Object
            return ['order']
        else:
            return []

    def get_exit_signals(self):
        if self.data_analyzer.get_latest_close() < self.data_analyzer.get_latest_sma():
            return ['ticker']
        else:
            return []

