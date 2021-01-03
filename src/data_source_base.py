# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

class DataSourceBase(object):
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def get_data(self):
        raise NotImplementedError