# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL

import asyncio as asy
import numpy as np
import logging

logger = logging.getLogger()

key = 'PKKPMD01L7WOTNX5Y62S'
secret = 'l2TXXSIz2AIjkSmUmXltYwicIZiBNU6kDpJ2pVxE'

class FakeAlpaca():
    def __init__(self):
        self.__stream = tradeapi.Stream(key, secret,
                                    base_url=URL('https://paper-api.alpaca.markets'),
                                    data_feed='iex')

    async def runforever(self):
        await self.__stream._run_forever()

    async def on_bars(self, data):
        logger.info(f'Received bar {data}')
        await asy.sleep(90)
        logger.info(f'Done sleeping')
        return "Test"

    async def get_bar(self):
        data = self.__stream.subscribe_bars(self.on_bars, 'AAPL')
        await self.runforever()
        logger.info(f'get_bar function executed')
        return data

class SimpleClass():
    def __init__(self):
        self._strategies = [1, 2, 3]
        print(self._strategies)
        logger.info('Initiated Simple Class')

    async def trade(self, alpaca):
       for strategy in self._strategies:
           bar = await alpaca.get_bar()
           print('Waiting in trade')
           print(bar)

async def main():
    simple = SimpleClass()
    alpaca = FakeAlpaca()

    while True:
        await simple.trade(alpaca)

if __name__ == "__main__":
    fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    fh = logging.FileHandler('console.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)

    loop = asy.get_event_loop()
    loop.run_until_complete(main())

