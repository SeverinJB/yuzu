# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import backtrader as bt

from test_resources.test_strategy import TestStrategy
from backtesting.yuzu_strategy_wrapper import YuzuStrategyWrapper
from backtesting.backtesting_data_collector import BacktestingDataCollector

class BackTraderTestStrategy(YuzuStrategyWrapper):
    def __init__(self):
        yuzu_strategy = TestStrategy(None)
        YuzuStrategyWrapper.__init__(self, yuzu_strategy)

def test_e2e_backtesting(capsys):
    ticker = 'YHOO'
    data = BacktestingDataCollector().get_data(
        ticker, start_data='2000-1-1', end_date='2000-12-31', frequency='daily')

    cerebro = bt.Cerebro()
    cerebro.optstrategy(
        BackTraderTestStrategy,
        maperiod=range(18, 21)
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.run(maxcpus=1)

    captured = capsys.readouterr()
    assert '(MA Period 18) Ending Value 646.80' in str(captured)
    assert '(MA Period 19) Ending Value 659.80' in str(captured)
    assert '(MA Period 20) Ending Value 650.80' in str(captured)
