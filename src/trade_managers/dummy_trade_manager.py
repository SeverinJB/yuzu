# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import trade_manager_base

class DummyTradeManager(trade_manager_base.TradeManagerBase):

    def _TradeManagerBase__buy(self, trade_data):
        print("I'm buying!")

    def _TradeManagerBase__sell(self, trade_data):
        print("I'm selling!")

    def close_position(self, id):
        print("I'm closing position '{}'!".format(id))

    def cancel_order(self, id):
        print("I'm canceling order '{}'!".format(id))

    def close_all(self):
        print("I'm closing all!")

    def cancel_all(self):
        print("I'm canceling all!")
