# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import enum


class Side(enum.Enum):
    BUY = 1
    SELL = 2


class Order:
    def __init__(self, strategy_name, ticker, side, size, valid_for_seconds, price=None,
                 stop_loss=None, take_profit=None, submitted_at=None):
        self.strategy = strategy_name
        self.ticker = ticker
        self.price = price
        self.side = side
        self.size = size
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.valid_for_seconds = valid_for_seconds
        self.submitted_at = submitted_at

    def convert_to_position(self):
        position = Position(
            strategy_name=self.strategy,
            ticker=self.ticker,
            price=self.price,
            side=self.side,
            size=self.size,
            stop_loss=self.stop_loss,
            take_profit=self.take_profit
        )

        return position


class Position(object):
    def __init__(self, strategy_name, ticker, price, side, size, stop_loss=None, take_profit=None,
                 avg_entry_price=None):
        self.strategy = strategy_name
        self.ticker = ticker
        self.price = price
        self.side = side
        self.size = size
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.avg_entry_price = avg_entry_price  # see #22

    def __eq__(self, other):
        return self.strategy == other.strategy \
               and self.ticker == other.ticker \
               and self.side == other.side


class Signal(object):
    def __init__(self, order, exits_position):
        self.order = order
        self.exits_position = exits_position
