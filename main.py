# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

# from session_managers.t212_session_manager import T212SessionManager
# from trade_executors.t212_trade_executor import T212TradeExecutor

from session_managers.alpaca_session_manager import AlpacaSessionManager
from trade_executors.alpaca_trade_executor import AlpacaTradeExecutor

import logging

logger = logging.getLogger()

from positions_manager import PositionsManager
from strategies_manager import StrategiesManager
from trade_manager import TradeManager

ALPACA_API_KEY = 'PKDCTVKOSWRFQGAUS8CY'
ALPACA_SECRET_KEY = 'Uhw8C9bX5ZXMX8eHfQuvKkMqgjjP6Rk0JLPzDQpp'

if __name__ == "__main__":
    #T212Session = T212SessionManager()
    #T212Session.login("tradingyuzu@gmail.com", "212TradingYuzu2020")
    #T212Trade = T212TradeExecuter(T212Session)

    fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    fh = logging.FileHandler('console.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)

    AlpacaSession = AlpacaSessionManager()
    AlpacaSession.login(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    AlpacaTrade = AlpacaTradeExecutor(AlpacaSession)

    strategiesManager = StrategiesManager(AlpacaSession)
    positionsManager = PositionsManager()

    tradeManager = TradeManager(AlpacaTrade, strategiesManager, positionsManager)

    while True:
        tradeManager.trade()