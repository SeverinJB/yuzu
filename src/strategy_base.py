# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

class StrategyBase(object):
    def __init__(self, data_analyzer, positions_manager, tickers=None):
        self.name = "strategy_base"
        self.data_analyzer = data_analyzer
        self.positions_manager = positions_manager
        self.tickers = tickers if tickers else []

    def get_open_positions(self):
        # TODO: write test for this method
        return self.positions_manager.get_open_positons_for_strategy(self.name)

    def get_name(self):
        return self.name

    def get_trade_signals(self):
        # Returns a list of signals
        raise NotImplementedError
