# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from trade_managers.dummy_trade_manager import DummyTradeManager as DTM
from trade_manager_base import Order, Side

if __name__ == "__main__":
    manager = DTM()

    buy_order = Order("TKR", Side.BUY, 100, 0, 20)
    sell_order = Order("TKR", Side.SELL, 100, 0, 20)
    manager.trade(buy_order)
    manager.trade(sell_order)

    manager.cancel_order(5)
    manager.close_position(3)
    manager.close_all()
    manager.cancel_all()