# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import enum

class Side(enum.Enum):
   BUY = 1
   SELL = 2
   NEUTRAL = 3

class Order:
    def __init__(self, ticker, trade_side, trade_size, stop, profit, open = None):
        self.ticker_symbol = ticker
        self.open_price = open
        self.side = trade_side
        self.size = trade_size
        self.stop_loss = stop
        self.take_profit = profit

class Position:
    def __init__(self, order):
        self.trade_order = order
        self.close_price = 0

class TradeManagerBase(object):
    def __init__(self):
        '''
        Contructor
        '''

        self.__pending_orders = {}
        self.__open_positions = {}
        self.__closed_positions = {}

    def __buy(self, order):
        raise NotImplementedError

    def __sell(self, order):
        raise NotImplementedError

    def close_position(self, id):
        raise NotImplementedError

    def cancel_order(self, id):
        raise NotImplementedError

    def close_all(self):
        raise NotImplementedError

    def cancel_all(self):
        raise NotImplementedError

    def trade(self, order):
        if order.side == Side.BUY:
            self.__buy(order)
        elif order.side == Side.SELL:
            self.__sell(order)

