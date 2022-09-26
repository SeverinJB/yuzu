# Copyright Yuzu Trading 2022
# Any unauthorised usage forbidden

# from session_managers.t212_session_manager import T212SessionManager
# from trade_executors.t212_trade_executor import T212TradeExecutor

import logging
import asyncio

from trades_manager import TradesManager
from brokers_manager import BrokersManager
from positions_manager import PositionsManager
from strategies_manager import StrategiesManager
from positions_aggregator import PositionsAggregator
from data_sources.alpaca_data_source import AlpacaDataSource
from session_managers.alpaca_session_manager import AlpacaSessionManager
from trade_executors.alpaca_trade_executor import AlpacaTradeExecutor

logger = logging.getLogger()

ALPACA_CREDENTIALS = ['PKKPMD01L7WOTNX5Y62S', 'l2TXXSIz2AIjkSmUmXltYwicIZiBNU6kDpJ2pVxE']


async def main():
    fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    fh = logging.FileHandler('console.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)

    brokers_manager = BrokersManager()
    brokers_manager.add_broker('alpaca', AlpacaSessionManager, AlpacaTradeExecutor,
                               AlpacaDataSource, PositionsManager(), ALPACA_CREDENTIALS)

    strategies_manager = StrategiesManager(brokers_manager)
    positions_aggregator = PositionsAggregator(brokers_manager)

    trade_manager = TradesManager(brokers_manager, strategies_manager, positions_aggregator)

    while True:
        await trade_manager.trade()


if __name__ == "__main__":
    asyncio.run(main())
