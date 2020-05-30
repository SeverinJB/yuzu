# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import time

from trade_managers.t212_trade_manager import T212TradeManager as T212Trade
from session_managers.t212_session_manager import T212SessionManager as T212Session
from trade_manager_base import Order, Side

if __name__ == "__main__":
    broker_account = T212Session()
    broker_account.login('tradingyuzu@gmail.com', '212TradingYuzu2020')

    broker = T212Trade(broker_account)
    broker.submit_order(Order(Side.BUY, '%24GERMAN30', 0.5, 12000))
