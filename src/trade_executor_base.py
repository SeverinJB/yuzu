# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

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

