# Copyright Yuzu Trading 2022
# Any unauthorised usage forbidden

import logging

logger = logging.getLogger()


class Broker(object):
    def __init__(self, name):
        self.name = name
        self.session = None
        self.trade_executor = None
        self.data_source = None
        self.positions_manager = None
