# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pandas as pd
import datetime

from data_source_base import DataSourceBase


class T212DataSource(DataSourceBase):
    def __init__(self, session_manager):
        super().__init__(session_manager)


    def __clean_data(self, data):
        tmp = {}

        for tick in data:
            tmp[datetime.datetime.strptime(tick['timestamp'], '%Y-%m-%dT%H:%M:%S%z').replace(
                tzinfo=None)] = {
                'bid': tick['bid'][
                    'close'], 'ask': tick['ask'][
                    'close'], 'volume': tick['volume']}

        clean_data = pd.DataFrame.from_dict(tmp, orient='index')

        return clean_data


    def get_historic_data(self, ticker, start, end):
        request_attributes = {'headers': self.session_manager.get_headers()}
        request_attributes['json'] = {'candles': [{'ticker': ticker, 'period': 'ONE_MINUTE',
                                                   'size': 500, 'includeFake': 'true'}]}

        request_url = 'https://demo.trading212.com/charting/v2/batch'

        response = self.session_manager.get_session().request(
            'POST', request_url, **request_attributes)

        data = self.__clean_data(response.json()['candles'][0]['result'])

        return data
