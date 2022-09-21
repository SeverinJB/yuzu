# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

import strategies_manager


@pytest.fixture
def test_strategies_manager(mocker):
    session_manager = mocker.Mock()
    positions_manager = mocker.Mock()
    manager = strategies_manager.StrategiesManager(session_manager, positions_manager)

    manager._StrategiesManager__strategies = {
        'MY_FIRST_STRATEGY': 'mock_first_strategy',
        'MY_SECOND_STRATEGY': 'mock_second_strategy'
    }

    return manager


def test_get_strategy_returns_correct_strategy(mock_strategies_manager):
    assert mock_strategies_manager.get_strategy('MY_FIRST_STRATEGY') == 'mock_first_strategy'


def test_get_strategies_returns_strategies(mock_strategies_manager):
    expected_return = mock_strategies_manager._StrategiesManager__strategies
    assert mock_strategies_manager.get_strategies() == expected_return


def test_select_strategies_creates_dict_of_strategies(mock_strategies_manager):
    # FIXME: How do you really test a function with changing output?
    mock_strategies_manager._StrategiesManager__strategies = None

    mock_strategies_manager._StrategiesManager__strategies = \
        mock_strategies_manager._StrategiesManager__select_strategies()

    assert isinstance(mock_strategies_manager._StrategiesManager__strategies, dict)
