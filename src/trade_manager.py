# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from positions_manager import Position

class TradeManager(object):
    def __init__(self, trade_executor, strategies_manager, positions_manager):
        self.__executor = trade_executor
        self.__strategies_manager = strategies_manager
        self.__positions_manager = positions_manager

    def __collect_trade_signals(self):
        signals = []
        for strategy in self.__strategies_manager.get_strategies().values():
            signals.extend(strategy.get_trade_signals())

        return signals

    def __classify_signals(self, signals):
        exit_orders = []
        entry_orders = []

        for signal in signals:
            if signal.exits_position:
                exit_orders.append(signal.order)
            else:
                entry_orders.append(signal.order)

        return exit_orders, entry_orders

    def __exit_positions(self, exit_orders):
        for order in exit_orders:
            print(order)
            order_response = self.__executor.submit_order(order)
            if order_response is not None:
                closed_size = order_response.order.size
                if closed_size == self.__positions_manager.get_open_position(
                        order.ticker_symbol).size:
                    self.__positions_manager.close_position(order.ticker_symbol)
                else:
                    # TODO: Implement and test this method
                    self.__positions_manager.update_position(order.ticker_symbol, closed_size)
            else:
                # TODO: Decide what to do if position cannot be opened
                raise Exception("TradeManager: failed to exit position!")

    def __enter_positions(self, entry_orders):
        for order in entry_orders:
            ticker = order.ticker_symbol
            if self.__positions_manager.ticker_is_busy(ticker):
                return
            order_response = self.__executor.submit_order(order)
            print(order_response.text)
            if order_response is not None:
                self.__positions_manager.open_position(order_response)
            else:
                # TODO: Decide what to do if position cannot be opened
                raise Exception("TradeManager: failed to enter position!")

    def trade(self):
<<<<<<< Updated upstream
        self.__positions_manager.update_positions()
        exit_orders, entry_orders = self.__classify_signals(self.__collect_trade_signals())
        self.__exit_positions(exit_orders)
        self.__enter_positions(entry_orders)
=======
        # self.__positions_manager.update_positions()
        exit_orders, entry_orders = classify_signals(self.__collect_trade_signals())
        #self.__exit_positions(exit_orders)
        #self.__enter_positions(entry_orders)

>>>>>>> Stashed changes
