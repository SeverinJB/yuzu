# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from trade_manager_base import TradeManagerBase, Side

class T212TradeManager(TradeManagerBase):
    def __init__(self, session_manager):
        super().__init__()
        self.__base_url = 'https://demo.trading212.com/rest'
        self.__session_manager = session_manager

    def _request(self, method, path, data=None, base_url=None, version='v2'):
        base_url = base_url or self.__base_url
        url = base_url + '/' + version + path

        headers = {
            'user-agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }

        opts = {'headers': headers}

        if method.upper() == 'GET':
            opts['params'] = data
        else:
            opts['json'] = data

        try:
            response = self.__session_manager.getSession().request(method, url, **opts)
            if response.text != '':
                return response.json()
        except Exception:
            print('Response failed.')

    def get(self, path, data=None):
        return self._request('GET', path, data)

    def post(self, path, data=None):
        return self._request('POST', path, data)

    def patch(self, path, data=None):
        return self._request('PATCH', path, data)

    def delete(self, path, data=None):
        return self._request('DELETE', path, data)

    def submit_order(self, order):
        '''Open a position'''
        # TODO: Implement different order types.

        url = '/pending-orders/entry-dep-limit-stop/' + order.ticker_symbol
        params = {
            "notify": "NONE",
            "targetPrice": order.open_price if order.side == Side.BUY else -order.open_price,
            "stopLoss": order.stop_loss,
            "takeProfit": order.take_profit,
            'quantity': order.size,
        }

        response = self.post(url, params)
        return response

    def cancel_order(self, order_id):
        '''Cancel an order'''
        self.delete('/pending-orders/entry/{}'.format(order_id))

    def cancel_all_orders(self):
        '''Cancel all open orders'''
        self.delete('/pending-orders/cancel')

    # TODO: Implement
    # def close_all_positions(self):
    # 	'''Liquidates all open positions at market price'''
    # 	self.delete('/open-positions/close-all/')
    # 	# return [Order(o) for o in resp]