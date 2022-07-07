# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from trade_executor_base import TradeExecutorBase
from trade_objects import Side

class T212TradeExecutor(TradeExecutorBase):
    def __init__(self, session_manager):
        super().__init__()
        self.__session_manager = session_manager

    def __send_request(
            self,
            request_type,
            path,
            request_data = None,
            base_url = 'https://demo.trading212.com/rest',
            api_version = 'v2'):

        request_attributes = {'headers': self.__session_manager.get_headers(),
                              'cookies': self.__session_manager.get_session().cookies.get_dict()}
        if request_type.upper() == 'GET':
            request_attributes['params'] = request_data
        else:
            request_attributes['json'] = request_data

        request_url = base_url + '/' + api_version + path
        response = self.__session_manager.get_session().request(
            request_type, request_url, **request_attributes)

        return response

    def __get(self, path, data = None):
        return self.__send_request('GET', path, data)

    def __post(self, path, data = None):
        return self.__send_request('POST', path, data)

    def __patch(self, path, data = None):
        return self.__send_request('PATCH', path, data)

    def __delete(self, path, data = None):
        return self.__send_request('DELETE', path, data)

    def submit_order(self, order):
        '''Open a position'''
        # TODO: Implement different order types.

        # TODO: Check response consistent with request

        path = '/pending-orders/entry-dep-limit-stop/' + order.ticker_symbol
        order_details = {
            "notify": "NONE",
            "targetPrice": order.price,
            "stopLoss": order.stop_loss,
            "takeProfit": order.take_profit,
            'quantity': order.size if order.side == Side.BUY else -order.size,
        }

        # TODO: confront with return requirements in trade_executor_base!
        return self.__post(path, order_details)

    def cancel_order(self, order_id):
        '''Cancel an order'''
        # TODO: Check response consistent with request
        self.__delete('/pending-orders/entry/{}'.format(order_id))

    def cancel_all_orders(self):
        # TODO: Check response consistent with request
        '''Cancel all open orders'''
        self.__delete('/pending-orders/cancel')

    # TODO: Implement
    # def close_all_positions(self):
        # TODO: Check response consistent with request
    # 	'''Liquidates all open positions at market price'''
    # 	self.delete('/open-positions/close-all/')
    # 	# return [Order(o) for o in resp]