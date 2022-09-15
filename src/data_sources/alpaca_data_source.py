# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import asyncio
import logging
import pandas as pd
import csv
from concurrent.futures import ProcessPoolExecutor

from alpaca_trade_api.rest import TimeFrame
from data_source_base import DataSourceBase

logger = logging.getLogger()

class AlpacaDataSource(DataSourceBase):
    def __init__(self, session_manager):
        super().__init__(session_manager)
        self.__session = self.session_manager.get_session()

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


    def get_data(self, ticker, start, end):
        response = self.__session.get_bars(ticker, TimeFrame.Minute, start, end, adjustment='raw')
        data = response.df

        return data


    def subscribe_bars(self, symbol):
        global call_api # "Can't pickle local object"
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

                with open(r'src/data_sources/alpaca_data.csv', 'a') as file:
                    writer = csv.DictWriter(file, fieldnames=field_names)
                    writer.writerow(data)
                    file.close()

        def call_api():
            self.session_manager.get_stream().subscribe_bars(on_bars, symbol)
            self.session_manager.get_stream().run()
            print(f'Subscribe Bars')

        loop.run_in_executor(executor, call_api)


    def get_latest_bars(self):
        data = []

        with open(r'src/data_sources/alpaca_data.csv', 'r') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for line in reader:
                data.append(line)

        return data


