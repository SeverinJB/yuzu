# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import backtrader as bt

from backtesting.backtesting_strategies import *
from backtesting.backtesting_data_collector import BacktestingDataCollector

def main():
    cerebro = bt.Cerebro()

    # cerebro.optstrategy(
    #     BackTraderTestStrategy,
    #     maperiod=range(18, 21)
    # )

    ticker = 'YHOO'
    data = BacktestingDataCollector().get_data(ticker)
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake = 10)

    # Set the commission
    cerebro.broker.setcommission(commission = 0.0)

    # Run over everything
    cerebro.run(maxcpus = 1)

if __name__ == "__main__":
    main()
