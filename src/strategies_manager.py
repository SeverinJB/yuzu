# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

from strategies.strategy_scalping import StrategyScalping
from data_sources.alpaca_data_source import AlpacaDataSource

import asyncio
import sys

class StrategiesManager(object):
    def __init__(self, session_manager):
        self.__session_manager = session_manager
        self.__strategies = self.__select_strategies()

    def __select_strategies(self):
        # It could be a dictionary {"strategy_name" : strategy instance}
        #strategies = {"strategy_scalping": StrategyScalping(AlpacaDataSource(
        #    self.__session_manager)}

        def main():
            symbols = ['AAPL']

            fleet = {}
            for symbol in symbols:
                algo = StrategyScalping(AlpacaDataSource(self.__session_manager), symbol,
                                        2000, self.__session_manager)
                fleet[symbol] = algo

            async def on_bars(data):
                if data.symbol in fleet:
                    fleet[data.symbol].on_bar(data)

            for symbol in symbols:
                AlpacaDataSource(
                    self.__session_manager).subscribe_bars(on_bars, symbol)

            async def on_trade_updates(data):
                #logger.info(f'trade_updates {data}')
                symbol = data.order['symbol']
                if symbol in fleet:
                    fleet[symbol].on_order_update(data.event, data.order)

            self.__session_manager.get_stream().subscribe_trade_updates(on_trade_updates)

            async def periodic():
                while True:
                    if not self.__session_manager.get_session().get_clock().is_open:
                        # logger.info('exit as market is not open')
                        sys.exit(0)
                    await asyncio.sleep(30)
                    positions = self.__session_manager.get_session().list_positions()
                    for symbol, algo in fleet.items():
                        pos = [p for p in positions if p.symbol == symbol]
                        algo.checkup(pos[0] if len(pos) > 0 else None)

            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.gather(
                self.__session_manager.get_stream()._run_forever(),
                periodic(),
            ))
            loop.close()

        strategies = {"strategy_scalping": main()}

        # select strategies, instantiate one for each with the
        # data source and add them to strategies
        return strategies

    def get_strategy(self, strategy_name):
        return self.__strategies[strategy_name]

    def get_strategies(self):
        return self.__strategies
