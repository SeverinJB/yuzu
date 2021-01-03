# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from indicator_base import IndicatorBase

class BollingerBands(IndicatorBase):
    def __init__(self):
        super().__init__()
        self.name = "bollinger_bands"

    def get_indicator(self, input_dataframe, n):
        # ddof=0 is required since
        # we want to take the standard deviation of the population and not sample

        dataframe = input_dataframe.copy()
        dataframe["moving_average"] = dataframe['bid'].rolling(n).mean()
        dataframe["BB_up"] = dataframe["moving_average"]+2 * dataframe['bid'].rolling(n).std(ddof=0)
        dataframe["BB_dn"] = dataframe["moving_average"]-2 * dataframe['bid'].rolling(n).std(ddof=0)
        dataframe["BB_width"] = dataframe["BB_up"] - dataframe["BB_dn"]
        dataframe.dropna(inplace=True)

        return dataframe