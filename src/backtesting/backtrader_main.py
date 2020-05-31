# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt

from backtesting.another_layer import *
from backtesting.backtesting_data_collector import BacktestingDataCollector

# Create a cerebro entity
cerebro = bt.Cerebro()

# Add a strategy
strats = cerebro.optstrategy(
    BackTraderTestStrategy,
    maperiod=range(18, 21))

# Add the Data Feed to Cerebro
cerebro.adddata(BacktestingDataCollector().get_data('YHOO'))

# Set our desired cash start
cerebro.broker.setcash(1000.0)

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=10)

# Set the commission
cerebro.broker.setcommission(commission=0.0)

# Run over everything
cerebro.run(maxcpus=1)