# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import enum

class Side(enum.Enum):
   BUY = 1
   SELL = 2
   NEUTRAL = 3

class Order:
    def __init__(self, ticker, side, trade_size, open, stop = None, profit = None):
        self.ticker_symbol = ticker
        self.open_price = open
        self.side = side
        self.size = trade_size
        self.stop_loss = stop
        self.take_profit = profit

class Position:
    def __init__(self, order):
        self.trade_order = order
        self.close_price = 0

class TradeExecutorBase(object):
    def __init__(self):
        pass

    def close_position(self, id):
        raise NotImplementedError

    def cancel_order(self, id):
        raise NotImplementedError

    def close_all(self):
        raise NotImplementedError

    def cancel_all(self):
        raise NotImplementedError

    def submit_order(self, order):
        raise NotImplementedError

