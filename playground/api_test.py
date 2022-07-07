# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pandas as pd
import alpaca_trade_api as alpaca
from alpaca_trade_api.rest import TimeFrame

now = pd.Timestamp.now(tz='America/New_York').floor('1min')
market_open = now.replace(hour=9, minute=30)
yesterday = (now - pd.Timedelta('1day')).strftime('%Y-%m-%dT%H:%M:%SZ')
today = (now).strftime('%Y-%m-%dT%H:%M:%SZ')
tomorrow = (now + pd.Timedelta('1day') - pd.Timedelta(minutes=20)).strftime('%Y-%m-%dT%H:%M:%SZ')

print(today , tomorrow)

ALPACA_API_KEY = 'PKV2G4ELHMMAD8C2WZEV'
ALPACA_SECRET_KEY = 'ssXejiB4kCSKcPEnvqgxOB5SGn4G3F8tl7f5aPyp'
symbol = 'AAPL'

api = alpaca.REST(key_id=ALPACA_API_KEY,
                  secret_key=ALPACA_SECRET_KEY,
                  base_url="https://paper-api.alpaca.markets")

data = api.get_bars(symbol, TimeFrame.Minute, today, today,
                    adjustment='raw').df

print(api.get_latest_trade(symbol).price)

print(data)