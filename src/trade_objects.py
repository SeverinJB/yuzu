# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import enum

class Side(enum.Enum):
   BUY = 1
   SELL = 2

class Order:
    def __init__(self, ticker, side, size, price=None, stop_loss=None, take_profit=None):
        self.ticker_symbol = ticker
        self.price = price
        self.side = side
        self.size = size
        self.stop_loss = stop_loss
        self.take_profit = take_profit

class Position(object):
    def __init__(self, strategy_name=None, order=None, id=None):
        self.strategy = strategy_name
        self.order = order
        self.trade_id = id

    def __eq__(self, other):
        return self.strategy == other.strategy \
               and self.trade_id == other.trade_id \
               and self.order == other.order

class Signal(object):
    def __init__(self, order, exits_position):
        self.order = order
        self.exits_position = exits_position
