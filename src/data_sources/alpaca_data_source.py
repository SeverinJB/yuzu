# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import asyncio
import logging
import pandas as pd
import csv
from concurrent.futures import ProcessPoolExecutor
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

    def subscribe_bars(self, symbol):
        global call_api  # "Can't pickle local object"
        loop = asyncio.get_running_loop()
        executor = ProcessPoolExecutor(max_workers=1)

        # TODO: on_bars(bar) should be __clean_data(data)
        async def on_bars(bar):
            if bar:
                field_names = ['open', 'high', 'low', 'close', 'volume', 'timestamp']

                data = {'open': bar.open,
                        'high': bar.high,
                        'low': bar.low,
                        'close': bar.close,
                        'volume': bar.volume,
                        'timestamp': pd.Timestamp(bar.timestamp)}

                logger.info(f'New bar: {pd.Timestamp(bar.timestamp)}, close: {bar.close}')

                with open(r'src/data_sources/alpaca_data.csv', 'a') as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)
                    writer.writerow(data)
                    file.close()

        def call_api():
            self.session_manager.get_stream().subscribe_bars(on_bars, symbol)
            self.session_manager.get_stream().run()
            print(f'Subscribe Bars')

        loop.run_in_executor(executor, call_api)

    def __append_bar(self, data, bar):
        data = data.append(pd.DataFrame({
            'open': float(bar["open"]),
            'high': float(bar["high"]),
            'low': float(bar["low"]),
            'close': float(bar["close"]),
            'volume': float(bar["volume"]),
        }, index=[pd.Timestamp(bar["timestamp"], tz=pytz.UTC)]))

        return data

    def get_latest_bars(self, ticker):
        with open(r'src/data_sources/alpaca_data.csv', 'r') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for bar in reader:
                if ticker not in self.__database.keys():
                    self.__database[ticker] = pd.DataFrame(columns=['timestamp', 'open', 'high',
                                                                    'low', 'close', 'volume'])
                    self.__database[ticker].set_index('timestamp', inplace=True)
                    self.__database[ticker] = self.__append_bar(self.__database[ticker], bar)
                elif pd.Timestamp(bar["timestamp"]) \
                        > pd.Timestamp(self.__database[ticker].index.values[-1]):
                    self.__database[ticker] = self.__append_bar(self.__database[ticker], bar)

        return self.__database[ticker]
