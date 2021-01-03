# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from indicator_base import IndicatorBase

class SimpleMovingAverage(IndicatorBase):
    def __init__(self):
        super().__init__()
        self.name = "simple_moving_average"

    def get_indicator(self, dataframe, period_slow, period_fast):
        dataframe['sma_slow'] = dataframe['bid'].rolling(period_slow).mean()
        dataframe['sma_fast'] = dataframe['bid'].rolling(period_fast).mean()
        return dataframe
