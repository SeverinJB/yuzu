# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategy_base import StrategyBase
from trade_objects import Side, Order, Signal

class TestStrategy(StrategyBase):
    def __init__(self, data_analyzer, positions_manager=None, tickers=None):
        super().__init__(data_analyzer, positions_manager, tickers)
        self.name = "strategy_test"

    def get_trade_signals(self):
        if self.data_analyzer.get_latest_close() > self.data_analyzer.get_latest_sma():
            order = Order("test_ticker", Side.BUY, 0)
            return [Signal(order, True)]
        elif self.data_analyzer.get_latest_close() < self.data_analyzer.get_latest_sma():
            order = Order("test_ticker", Side.SELL, 0)
            return [Signal(order, False)]
        else:
            return []

