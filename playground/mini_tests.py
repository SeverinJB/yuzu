# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL

key = 'PKKPMD01L7WOTNX5Y62S'
secret = 'l2TXXSIz2AIjkSmUmXltYwicIZiBNU6kDpJ2pVxE'
base_url = URL('https://paper-api.alpaca.markets')
symbol = 'AAPL'

session = tradeapi.REST(key, secret, base_url)

float_price = float(session.get_latest_trade(symbol).price)
current_price = session.get_latest_trade(symbol)

print(current_price.price)