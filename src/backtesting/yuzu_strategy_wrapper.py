# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import backtrader as bt

from data_analyzers.back_trader_data_analyzer import BackTraderDataAnalyzer

class YuzuStrategyWrapper(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('printlog', False),
    )

    def __init__(self, yuzu_strategy):
        super().__init__()
        data_analyzer = BackTraderDataAnalyzer(self.datas)
        data_analyzer.add_sma(self.params.maperiod)
        self.__yuzu_strategy = yuzu_strategy
        self.__yuzu_strategy.data_analyzer = data_analyzer

        self.order = None
        self.buyprice = None
        self.buycomm = None

    def __log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            if self.__yuzu_strategy.get_entry_signals():
                self.order = self.buy()
        else:
            if self.__yuzu_strategy.get_exit_signals():
                self.order = self.sell()

    def stop(self):
        self.__log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.__log('Order Canceled/Margin/Rejected')

        self.order = None
