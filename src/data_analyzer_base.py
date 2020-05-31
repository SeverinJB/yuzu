# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

class DataAnalyzerBase(object):
    def __init__(self, data_source):
        self.data_source = data_source

    def get_latest_close(self):
        raise NotImplementedError

    def get_latest_sma(self):
        raise NotImplementedError
