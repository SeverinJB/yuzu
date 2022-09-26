# Copyright Yuzu Trading 2022
# Any unauthorised usage forbidden

import logging

logger = logging.getLogger()


class PositionsManager(object):
    def __init__(self):
        self.__open_positions = {}  # {'TICKER': POSITION}
        self.__pending_orders = {}  # {'TICKER': ORDER}


    def update_order(self, event, order_update):
        ticker = order_update['symbol']
        logger.info(f"order update: {event} = {order_update}")

        pending_order = self.get_pending_order_for_ticker(ticker)
        open_position = self.get_open_position_for_ticker(ticker)

        if pending_order:
            if order_update['id'] == pending_order.broker_order_id:
                if event == 'fill':
                    position = pending_order.convert_to_position()
                    position.avg_entry_price = order_update['filled_avg_price']
                    position.size = int(order_update['filled_qty'])

                    if open_position:
                        self.update_position(open_position, position)
                    else:
                        self.open_position(position)

                elif event == 'partial_fill':
                    remaining_order = pending_order
                    remaining_order.size -= int(order_update['filled_qty'])

                    position = pending_order.convert_to_position()
                    position.avg_entry_price = order_update['filled_avg_price']
                    position.size = int(order_update['filled_qty'])

                    if open_position:
                        self.update_position(open_position, position)
                    else:
                        self.open_position(position)

                    self.add_order(remaining_order)

                elif event in ('canceled', 'rejected'):
                    if event == 'rejected':
                        logger.warn(f"Order rejected: current order = {order_update}")

                    self.delete_order(ticker)

                else:
                    logger.warn(f"Unexpected event: {event} for {order_update}")
            else:
                logger.warn(f"Unexpected update: No pending order with this id, {order_update}")
        else:
            logger.warn(f"Unexpected update: No pending order for {ticker}")


    def update_position(self, open_position, position):
        if open_position.side == position.side:
            open_position.size += position.size
            avg_entry_price = (open_position.avg_entry_price + position.avg_entry_price)/2
            open_position.avg_entry_price = avg_entry_price
        else:
            open_position.size -= position.size


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
        if ticker in self.__open_positions.keys():
            return self.__open_positions[ticker]
        else:
            return None


    def get_pending_order_for_ticker(self, ticker):
        if ticker in self.__pending_orders.keys():
            return self.__pending_orders[ticker]
        else:
            return None


    def get_open_positions(self):
        return self.__open_positions


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
