# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL

from trade_objects import Order

test_order = Order('strategy_name', 'ticker', 'side', 'size', 'valid_for_seconds')

print(test_order)

test_position = test_order.convert_to_position()

print(test_position)