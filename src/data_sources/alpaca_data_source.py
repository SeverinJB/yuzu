# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import pytz
import logging
import pandas as pd
from alpaca_trade_api.rest import TimeFrame

from data_source_base import DataSourceBase

logger = logging.getLogger()


class AlpacaDataSource(DataSourceBase):
    def __init__(self, session_manager):
        super().__init__(session_manager)
        self.__session = self.session_manager.get_session()
        self.__database = {}  # {'TICKER': DATAFRAME, ...}
        self.__bars = {}  # {'TICKER': [BAR_1, BAR_2, BAR_3, ...], ...}


    def get_latest_trade(self, ticker):
        return self.__session.get_latest_trade(ticker)


    def __clean_data(self, data):
        raise NotImplementedError


    def __append_bar(self, data, bar):
        data = data.append(pd.DataFrame({
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume,
        }, index=[pd.Timestamp(bar.timestamp, tz=pytz.UTC)]))

        return data


    def get_historic_data(self, ticker, start, end):
        response = self.__session.get_bars(ticker, TimeFrame.Minute, start, end, adjustment='raw')
        data = response.df

        return data


    def subscribe_bars(self, ticker):
        if ticker not in self.__database.keys():
            column_names = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            self.__database[ticker] = pd.DataFrame(columns=column_names)
            self.__database[ticker].set_index('timestamp', inplace=True)

        if ticker not in self.__bars.keys():
            self.__bars[ticker] = []

        async def on_bar(bar):
            if bar:
                self.__bars[ticker].append(bar)

                # bar.timestamp is one minute behind __now() as bar concerns previous minute.
                logger.info(f'New bar: {pd.Timestamp(bar.timestamp)}, close: {bar.close}, '
                            f'len(database[{ticker}]): {len(self.__database[ticker].index)}')

        self.session_manager.get_stream().subscribe_bars(on_bar, ticker)


    async def get_latest_bars(self, ticker):
        if self.__bars[ticker]:
            # TODO: Implement quicker solution for appending long list of bars.
            for bar in self.__bars[ticker]:
                self.__database[ticker] = self.__append_bar(self.__database[ticker], bar)
                self.__bars[ticker].remove(bar)
            return self.__database[ticker]
        else:
            return None
