# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import asyncio
import logging
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
        global call_api
        loop = asyncio.get_running_loop()
        executor = ProcessPoolExecutor()

        async def on_bars(data):
            print(data)

        def call_api():
            self.session_manager.get_stream().subscribe_bars(on_bars, symbol)
            self.session_manager.get_stream().run()

        loop.run_in_executor(executor, call_api)

        print(f'Subscribe Bars')

        return None


    def get_data(self, ticker, start, end):
        response = self.session_manager.get_session().get_bars(ticker, TimeFrame.Minute,
                                                               start, end,
                                                               adjustment='raw')

        data = response.df

        return data
