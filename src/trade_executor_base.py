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

class TradeExecutorBase(object):
    def __init__(self):
        pass

    def close_position(self, id):
        # Must return a bool indicating whether or not the closure was successful
        raise NotImplementedError

    def cancel_order(self, id):
        raise NotImplementedError

    def close_all(self):
        raise NotImplementedError

    def cancel_all(self):
        raise NotImplementedError

    def submit_order(self, order):
        # must return an order object which contains the onfo of the performed order
        # if something goes wrong, it must return None
        raise NotImplementedError

