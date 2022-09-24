# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

import logging

logger = logging.getLogger()


class PositionsManager(object):
    def __init__(self):
        # TODO: Implement new dictionary structure.
        self.__open_positions = {}  # {'EXECUTOR': {'TICKER': ORDER}, ...}
        self.__pending_orders = {}  # {'EXECUTOR': {'TICKER': ORDER}, ...}


    def update_position(self, ticker, update):
        logger.info(f"order update: {update['event']} = {update['order']}")

        if update['event'] == 'fill':
            position = self.get_pending_order_for_ticker(ticker).convert_to_position()
            position.avg_entry_price = update['order']['filled_avg_price']  # #22

            self.open_position(position)

        elif update['event'] == 'partial_fill':
            remaining_order = self.get_pending_order_for_ticker(ticker)
            remaining_order.size -= int(update['order']['filled_qty'])

            position = self.get_pending_order_for_ticker(ticker).convert_to_position()
            position.size = int(update['order']['filled_qty'])
            position.avg_entry_price = update['order']['filled_avg_price']  # #22

            self.open_position(position)
            self.add_order(remaining_order)

        elif update['event'] in ('canceled', 'rejected'):
            if update['event'] == 'rejected':
                logger.warn(f"Order rejected: current order = {update['order']}")

            self.delete_order(ticker)

        else:
            logger.warn(f"Unexpected event: {update['event']} for {update['order']}")


    def open_position_exists_for_ticker(self, ticker):
        return ticker in self.__open_positions


    def pending_order_exists_for_ticker(self, ticker):
        return ticker in self.__pending_orders


    def ticker_is_busy(self, ticker):
        return self.open_position_exists_for_ticker(ticker) or \
               self.pending_order_exists_for_ticker(ticker)


    def get_open_positions_for_strategy(self, strategy_name):
        positions = []
        for position in self.__open_positions.values():
            if position.strategy == strategy_name:
                positions.append(position)

        return positions


    def get_open_position_for_ticker(self, ticker):
        return self.__open_positions[ticker]


    def get_pending_order_for_ticker(self, ticker):
        return self.__pending_orders[ticker]


    def get_pending_orders(self):
        return self.__pending_orders


    def open_position(self, position):
        # TODO: If ticker already busy for strategy, add new order to existing position.
        #       However, strategy and executor can only have one position.
        ticker = position.ticker
        self.delete_order(ticker)
        self.__open_positions[ticker] = position
        logger.info(f'Open position: {position}')


    def close_position(self, ticker):
        if ticker in self.__open_positions:
            del self.__open_positions[ticker]
        else:
            raise Exception(f'PositionsManager: No existing position for {ticker}!')


    def add_order(self, order):
        ticker = order.ticker
        if ticker in self.__pending_orders:
            raise Exception(f'PositionsManager: Already pending order for {ticker}!')
        else:
            self.__pending_orders[ticker] = order
            logger.info(f'Open pending order: {order}')


    def delete_order(self, ticker):
        if ticker in self.__pending_orders:
            del self.__pending_orders[ticker]
        else:
            raise Exception(f'PositionsManager: No pending order for {ticker}!')
