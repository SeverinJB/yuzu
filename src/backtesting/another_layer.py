# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategies.strategy_test import StrategyTest
# from strategies.strategy_A import StrategyA
# from strategies.strategy_B import StrategyB

import backtrader as bt

from strategies.strategy_test import StrategyTest
from backtesting.backtrader_test_strategy import BacktraderStrategyBase

class BackTraderTestStrategy(BacktraderStrategyBase):
    def __init__(self):
        yuzu_strategy = StrategyTest(None)
        BacktraderStrategyBase.__init__(self, yuzu_strategy)