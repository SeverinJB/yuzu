# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL
from alpaca_trade_api.stream import Stream
from concurrent.futures import ThreadPoolExecutor

import logging
import asyncio
import pandas as pd

logger = logging.getLogger()

ALPACA_API_KEY = 'PKKPMD01L7WOTNX5Y62S'
ALPACA_SECRET_KEY = 'l2TXXSIz2AIjkSmUmXltYwicIZiBNU6kDpJ2pVxE'

executor = ThreadPoolExecutor(max_workers=1)

fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=fmt)
fh = logging.FileHandler('console.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(fmt))
logger.addHandler(fh)

global stream
stream = None

trade_status = {}

async def bars_callback(bar):
    print(bar)
    logger.info(f'New bar: {pd.Timestamp(bar.timestamp)}, close: {bar.close},')


async def print_update(data):
    if data.order['symbol'] not in trade_status.keys():
        trade_status[data.order['symbol']] = []

    trade_status[data.order['symbol']].append(data)


def start_stream():
    global stream

    if not stream:
        stream = Stream(ALPACA_API_KEY, ALPACA_SECRET_KEY,
                        base_url=URL('https://paper-api.alpaca.markets'),
                        data_feed='iex')  # <- replace to 'sip' if you have PRO subscription
        stream.subscribe_bars(bars_callback, 'IBM')
        stream.subscribe_trade_updates(print_update)

        executor.submit(stream.run)


while True:
    print(trade_status)
    start_stream()

