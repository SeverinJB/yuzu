# Copyright Burg&Biondi 2020
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


    def __clean_data(self, data):
        raise NotImplementedError


    def subscribe_bars(self, symbol):
        global call_api # "Can't pickle local object"
        loop = asyncio.get_running_loop()
        executor = ProcessPoolExecutor(max_workers=1)

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

        return None


    def get_latest_bars(self):
        data = []

        with open(r'src/data_sources/alpaca_data.csv', 'r') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for line in reader:
                data.append(line)

        return data


    def get_data(self, ticker, start, end):
        response = self.session_manager.get_session().get_bars(ticker, TimeFrame.Minute,
                                                               start, end,
                                                               adjustment='raw')

        data = response.df

        return data
