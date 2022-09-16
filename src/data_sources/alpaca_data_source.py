# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import pytz

from alpaca_trade_api.rest import TimeFrame
from data_source_base import DataSourceBase

logger = logging.getLogger()


class AlpacaDataSource(DataSourceBase):
    def __init__(self, session_manager):
        super().__init__(session_manager)
        self.__session = self.session_manager.get_session()
        self.__database = {}  # Ticker is key


    # TODO: Must be removed. Handled by trade_executor
    def list_orders(self):
        return self.__session.list_orders()


    # TODO: Must be removed. Handled by trade_executor
    def list_positions(self):
        return self.__session.list_positions()


    def get_latest_trade(self, symbol):
        return self.__session.get_latest_trade(symbol)


    def __clean_data(self, data):
        raise NotImplementedError


    def get_historic_data(self, ticker, start, end):
        response = self.__session.get_bars(ticker, TimeFrame.Minute, start, end, adjustment='raw')
        data = response.df

        return data


    def __append_bar(self, data, bar):
        data = data.append(pd.DataFrame({
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume,
        }, index=[pd.Timestamp(bar.timestamp, tz=pytz.UTC)]))

        return data


    def subscribe_bars(self, symbol):
        global start_data_stream  # "Can't pickle local object"
        executor = ThreadPoolExecutor(max_workers=1)

        if symbol not in self.__database.keys():
            columnn_names = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            self.__database[symbol] = pd.DataFrame(columns=columnn_names)
            self.__database[symbol].set_index('timestamp', inplace=True)

        async def on_bar(bar):
            if bar:
                logger.info(f'New bar: {pd.Timestamp(bar.timestamp)}, close: {bar.close}')
                self.__database[symbol] = self.__append_bar(self.__database[symbol], bar)

        def start_data_stream():
            self.session_manager.get_stream().subscribe_bars(on_bar, symbol)
            self.session_manager.get_stream().run()

        executor.submit(start_data_stream)


    async def get_latest_bars(self, ticker):
        return self.__database[ticker]
