# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL

import session_manager_base


class AlpacaSessionManager(session_manager_base.SessionManagerBase):
    def __init__(self):
        self.__session = None
        self.__stream = None
        self.__base_url = URL('https://paper-api.alpaca.markets')

    def login(self, key, secret):
        self.__session = tradeapi.REST(key, secret, self.__base_url)
        self.__stream = tradeapi.Stream(key, secret,
                        base_url=self.__base_url,
                        data_feed='iex') # <- replace to sip for PRO subscription

    def logout(self):
        raise NotImplementedError

    def get_session(self):
        return self.__session

    def get_stream(self):
        return self.__stream
