# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import tiingo
import backtrader as bt

class BacktestingDataCollector():
    def __init__(self):
        self.__tiingo_client = tiingo.TiingoClient(
            {'session': True, 'api_key': '99af266961f0e99c420003305a57088fd8a08d1e'})

    def get_data(self, ticker_symbol, start_data='2000-1-1', end_date='2000-12-31',
                 frequency='daily'):

        dataframe = self.__tiingo_client.get_dataframe(ticker_symbol,
                                                     startDate=start_data,
                                                     endDate=end_date, frequency=frequency)

        dataframe = dataframe[['adjClose', 'adjHigh','adjLow', 'adjOpen', 'adjVolume']]
        dataframe.columns = ['close', 'high', 'low', 'open', 'volume']

        dataframe.sort_index(inplace=True)
        data = bt.feeds.PandasData(dataname=dataframe)

        return data
