# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from alpaca_trade_api.rest import TimeFrame
import pandas as pd

from data_source_base import DataSourceBase


class AlpacaDataSource(DataSourceBase):
    def __init__(self, session_manager):
        super().__init__(session_manager)

    def __clean_data(self, data):
        raise NotImplementedError

    def subscribe_bars(self, on_bars, symbol):
        data = self.session_manager.get_stream().subscribe_bars(on_bars, symbol)

        return data

    def get_data(self, ticker):
        now = pd.Timestamp.now(tz='America/New_York').floor('1min')
        start = (now - pd.Timedelta('1day')).strftime('%Y-%m-%dT%H:%M:%SZ')
        end = (now).strftime('%Y-%m-%dT%H:%M:%SZ')
        response = self.session_manager.get_session().get_bars(ticker, TimeFrame.Minute,
                                                               start, end,
                                                               adjustment='raw')

        print(response)
        data = response.df

        return data
