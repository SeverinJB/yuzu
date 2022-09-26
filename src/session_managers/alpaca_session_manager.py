# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging
import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL
from concurrent.futures import ThreadPoolExecutor

import session_manager_base

logger = logging.getLogger()


class AlpacaSessionManager(session_manager_base.SessionManagerBase):
    def __init__(self):
        self.name = 'alpaca_session'
        self.__session = None
        self.__stream = None
        self.__base_url = URL('https://paper-api.alpaca.markets')


    def __start_stream(self, key, secret):
        executor = ThreadPoolExecutor(max_workers=1)

        self.__stream = tradeapi.Stream(key, secret,
                        base_url=self.__base_url,
                        data_feed='iex')  # <- replace to sip for PRO subscription

        executor.submit(self.__stream.run)


    def login(self, credentials):
        key, secret = credentials
        self.__session = tradeapi.REST(key, secret, self.__base_url)
        self.__start_stream(key, secret)


    def logout(self):
        raise NotImplementedError


    def get_session(self):
        return self.__session


    def get_stream(self):
        return self.__stream
