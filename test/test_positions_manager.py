# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

from positions_manager import PositionsManager
from trade_objects import Position

def test_open_position_exists_for_ticker_returns_true_if_open_position_for_ticker_exists():
    ticker = 'MY_TICKER'
    open_positions = {ticker : 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__open_positions = open_positions

    assert manager.open_position_exists_for_ticker(ticker)

def test_open_position_exists_for_ticker_returns_false_if_open_position_for_ticker_does_not_exist():
    ticker = 'MY_TICKER'
    open_positions = {ticker : 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__open_positions = open_positions

    assert not manager.open_position_exists_for_ticker('ANOTHER_TICKER')

def test_pending_order_exists_for_ticker_returns_true_if_pending_order_for_ticker_exists():
    ticker = 'MY_ORDER_TICKER'
    pending_order = {ticker : 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__pending_orders = pending_order

    assert manager.pending_order_exists_for_ticker(ticker)

def test_pending_order_exists_for_ticker_returns_false_if_pending_order_for_ticker_does_not_exist():
    ticker = 'MY_ORDER_TICKER'
    pending_order = {ticker : 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__pending_orders = pending_order

    assert not manager.pending_order_exists_for_ticker('ANOTHER_TICKER')

def test_ticker_is_busy_returns_true_if_position_is_open_for_ticker():
    ticker = 'MY_TICKER'
    open_positions = {ticker: 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__open_positions = open_positions

    assert manager.ticker_is_busy(ticker)

def test_ticker_is_busy_returns_true_if_order_is_pending_for_ticker():
    ticker = 'MY_ORDER_TICKER'
    pending_orders = {ticker: 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__pending_orders = pending_orders

    assert manager.ticker_is_busy(ticker)
    
def test_ticker_is_busy_returns_false_if_ticker_is_free():
    manager = PositionsManager()
    manager._PositionsManager__open_positions = {'POSITION_TICKER': 'mock_position'}
    manager._PositionsManager__pending_orders = {'ORDER_TICKER': 'mock_position'}

    assert not manager.ticker_is_busy('FREE_TICKER')

def test_get_open_positons_for_strategy_gets_all_position_for_strategy():
    position_strategy_a_1 = Position('strategyA', 'mock_order1', 0)
    position_strategy_a_2 = Position('strategyA', 'mock_order2', 1)
    position_strategy_b_1 = Position('strategyB', 'mock_order3', 2)
    open_positions = {
        'TK1' : position_strategy_a_1,
        'TK2' : position_strategy_a_2,
        'TK3' : position_strategy_b_1
    }

    expected_positions = [position_strategy_a_1, position_strategy_a_2]

    manager = PositionsManager()
    manager._PositionsManager__open_positions = open_positions

    assert manager.get_open_positons_for_strategy('strategyA') == expected_positions

def test_get_open_position_returns_correct_position():
    manager = PositionsManager()
    ticker = 'POSITION_TICKER'
    position = 'mock_position'
    manager._PositionsManager__open_positions = {ticker : position}

    assert manager.get_open_position(ticker) == position

def test_get_pending_order_returns_correct_position():
    manager = PositionsManager()
    ticker = 'ORDER_TICKER'
    position = 'mock_position'
    manager._PositionsManager__pending_orders = {ticker : position}

    assert manager.get_pending_order(ticker) == position

def test_open_position_opens_position(mocker):
    mock_order = mocker.Mock()
    mock_order.ticker_symbol = 'TEST_TICKER'
    position = Position('strategy', mock_order, 0)

    manager = PositionsManager()
    manager.open_position(position)

    assert manager._PositionsManager__open_positions['TEST_TICKER'] == position

# TODO: Update Position related test
def test_open_position_raise_error_if_ticker_already_busy(mocker):
    mock_order = mocker.Mock()
    ticker = 'TEST_TICKER'
    mock_order.ticker_symbol = ticker
    position = Position('strategy', mock_order, 0)

    manager = PositionsManager()
    manager._PositionsManager__open_positions = {ticker : position}

    with pytest.raises(Exception):
        manager.open_position(position)

def test_close_position_closes_position():
    ticker = 'MY_TICKER'
    open_positions = {ticker: 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__open_positions = open_positions

    manager.close_position(ticker)

    assert len(manager._PositionsManager__open_positions) == 0

def test_close_position_raises_if_position_does_not_exist():
    ticker = 'MY_TICKER'
    open_positions = {ticker: 'mock_position'}

    manager = PositionsManager()
    manager._PositionsManager__open_positions = open_positions

    with pytest.raises(Exception):
        manager.close_position('NOT_EXISTING_TICKER')
