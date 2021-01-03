# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from trade_executors.t212_trade_executor import T212TradeExecutor as T212Trade
from positions_manager import PositionsManager
from session_managers.t212_session_manager import T212SessionManager
from strategies_manager import StrategiesManager
from trade_manager import TradeManager

if __name__ == "__main__":
    T212Session = T212SessionManager()
    T212Session.login("tradingyuzu@gmail.com", "212TradingYuzu2020")

    t212Trade = T212Trade(T212Session)
    strategiesManager = StrategiesManager(T212Session)
    positionsManager = PositionsManager()

    tradeManager = TradeManager(t212Trade, strategiesManager, positionsManager)

    while True:
        tradeManager.trade()