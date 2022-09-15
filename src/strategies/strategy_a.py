# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategy_base import StrategyBase
from trade_objects import Side, Order, Signal
from indicators.simple_moving_average import SimpleMovingAverage as SMA

class StrategyA(StrategyBase):
    def __init__(self, data_analyzer=None, positions_manager=None, tickers=None):
        super().__init__(data_analyzer, positions_manager, tickers)
        self.name = "strategy_a"

        ### TODO: CLEAN UP

    def __data(self):
        self.df = self.data_analyzer.get_historic_data('GOOG')

        # self.sma = SMA.get_indicator(self, self.df, 50, 200)

    def get_trade_signals(self):
        #order = Order('Fake', Side.BUY, 10)

        self.__data()

        #if self.sma['bid'].iat[-1] > self.sma['sma_fast'].iat[-1]:
            #print("BIGGER", self.sma['bid'].iat[-1], self.sma['sma_fast'].iat[-1])
            #order = Order('GOOG', Side.SELL, 0.1, price=self.sma['bid'].iat[-1])

        #elif self.sma['bid'].iat[-1] < self.sma['sma_fast'].iat[-1]:
            #print("SMALLER", self.sma['bid'].iat[-1], self.sma['sma_fast'].iat[-1])
            #order = Order('GOOG', Side.SELL, 0.1, price=self.sma['bid'].iat[-1])

        order = Order('GOOG', Side.SELL, 0.1, price=self.df['high'].iat[-1])

        return [Signal(order, False)]