# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from trade_executors.t212_trade_executor import T212TradeExecutor as T212Trade
from session_managers.t212_session_manager import T212SessionManager as T212Session
from trade_executor_base import Order, Side

if __name__ == "__main__":
    login()
    strategies = SM.selectStrategies()
    tradeManager = TM(strategies)

    while True:
        tradeManager.trade()
