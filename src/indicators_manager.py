# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from indicators.simple_moving_average import SimpleMovingAverage
from indicators.bollinger_bands import BollingerBands

class IndicatorManager(object):
    def __init__(self):
        print("Indicator Manager")
        self.__indicators = self.__select_indicators()

    def __select_indicators(self):
        # It could be a dictionary {"indicator_name" : indicator instance}
        indicators = {'simple_moving_average': SimpleMovingAverage(),
                      'bollinger_bands': BollingerBands()}
        # select indicator, instantiate one for each
        return indicators

    def get_indicator(self, indicator_name):
        return self.__indicators[indicator_name]
