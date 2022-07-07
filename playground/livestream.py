# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL

async def trade_callback(t):
    print('trade', t)


async def quote_callback(q):
    print('quote', q)


# Initiate Class Instance
stream = Stream('PKV2G4ELHMMAD8C2WZEV',
                'ssXejiB4kCSKcPEnvqgxOB5SGn4G3F8tl7f5aPyp',
                base_url=URL('https://paper-api.alpaca.markets'),
                data_feed='iex')

# subscribing to event
stream.subscribe_trades(trade_callback, 'AAPL')
stream.subscribe_trades(quote_callback, 'AAPL')

stream.run()

