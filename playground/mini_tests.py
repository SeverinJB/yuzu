# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pandas as pd

before_market = pd.Timestamp.now(tz='America/New_York').floor('1min').time() <= pd.Timestamp(
    '09:30').time()
after_market = pd.Timestamp.now(tz='America/New_York').floor('1min').time() >= pd.Timestamp(
    '16:00').time()

market_closed = before_market or after_market

print(market_closed)