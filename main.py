# Copyright Yuzu Trading 2022
# Any unauthorized usage forbidden

# from session_managers.t212_session_manager import T212SessionManager
# from trade_executors.t212_trade_executor import T212TradeExecutor

import logging
import asyncio

from positions_manager import PositionsManager
from strategies_manager import StrategiesManager
from trades_manager import TradeManager
from session_managers.alpaca_session_manager import AlpacaSessionManager
from trade_executors.alpaca_trade_executor import AlpacaTradeExecutor

logger = logging.getLogger()

ALPACA_API_KEY = 'PKKPMD01L7WOTNX5Y62S'
ALPACA_SECRET_KEY = 'l2TXXSIz2AIjkSmUmXltYwicIZiBNU6kDpJ2pVxE'


async def main():
    fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    fh = logging.FileHandler('console.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)

    alpacaSession = AlpacaSessionManager()
    alpacaSession.login(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    alpacaTrade = AlpacaTradeExecutor(alpacaSession)

    positionsManager = PositionsManager()
    strategiesManager = StrategiesManager(alpacaSession, positionsManager)
    tradeManager = TradeManager(alpacaTrade, strategiesManager, positionsManager)

    while True:
        await tradeManager.trade()


if __name__ == "__main__":
    asyncio.run(main())
