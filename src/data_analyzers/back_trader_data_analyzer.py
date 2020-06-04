# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import backtrader as bt

from data_analyzer_base import DataAnalyzerBase

class BackTraderDataAnalyzer(DataAnalyzerBase):
    def __init__(self, data):
        super().__init__(data)
        self.__close = data[0].close

    def add_sma(self, period):
        self.__sma = bt.indicators.SimpleMovingAverage(self.data_source[0], period=period)

    def get_latest_close(self):
        return self.__close[0]

    def get_latest_sma(self):
        return self.__sma[0]
