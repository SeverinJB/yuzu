# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

import strategies_manager

def test_get_strategy_returns_correct_strategy():
    manager = strategies_manager.StrategiesManager(None)
    manager._StrategyManager__strategies = {'strategyA' : 'StrategyA_Object'}

    assert manager.get_strategy('strategyA') == 'StrategyA_Object'

def test_get_strategies_returns_strategies():
    manager = strategies_manager.StrategiesManager(None)
    expected_strategies = {
        'strategyA' : 'StrategyA_Object', 'strategyB' : 'StrategyB_Object'}
    manager._StrategyManager__strategies = expected_strategies

    assert manager.get_strategies() == expected_strategies

# TODO: Add test for strategies selection once implemented
