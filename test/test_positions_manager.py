# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

from positions_manager import PositionsManager


@pytest.fixture
def test_positions_manager():
    manager = PositionsManager()

    ticker = 'MY_TICKER'
    open_positions = {ticker: 'mock_position'}
    manager._PositionsManager__open_positions = open_positions

    order_ticker = 'MY_ORDER_TICKER'
    pending_orders = {order_ticker: 'mock_order'}
    manager._PositionsManager__pending_orders = pending_orders

    return manager


def test_update_position_creates_position_for_filled_order(mocker, test_positions_manager):
    open_positions = test_positions_manager._PositionsManager__open_positions

    order = mocker.Mock()
    order.ticker = 'MY_ORDER_TICKER'

    update = {'event': 'fill', 'order': order}
    test_positions_manager.update_position(update)

    assert open_positions['MY_ORDER_TICKER'] == update['order']


def test_update_position_creates_pending_order_for_partial_fill(mocker, test_positions_manager):
    pending_orders = test_positions_manager._PositionsManager__pending_orders

    ticker = 'MY_ORDER_TICKER'

    existing_order = mocker.Mock()
    existing_order.ticker = ticker
    existing_order.size = 5

    pending_orders[ticker] = existing_order

    partial_fill_order = mocker.Mock()
    partial_fill_order.ticker = ticker
    partial_fill_order.size = 2

    update = {'event': 'partial_fill', 'order': partial_fill_order}
    test_positions_manager.update_position(update)

    assert pending_orders[ticker].size == 3


def test_update_position_creates_open_position_for_partial_fill(mocker, test_positions_manager):
    pending_orders = test_positions_manager._PositionsManager__pending_orders
    open_positions = test_positions_manager._PositionsManager__open_positions

    ticker = 'MY_ORDER_TICKER'

    existing_order = mocker.Mock()
    existing_order.ticker = ticker
    existing_order.size = 5

    pending_orders[ticker] = existing_order

    partial_fill_order = mocker.Mock()
    partial_fill_order.ticker = ticker
    partial_fill_order.size = 2

    update = {'event': 'partial_fill', 'order': partial_fill_order}
    test_positions_manager.update_position(update)

    assert open_positions[ticker].size == 2


def test_update_position_deletes_pending_order_for_rejected(mocker, test_positions_manager):
    pending_orders = test_positions_manager._PositionsManager__pending_orders

    rejected_order = mocker.Mock()
    rejected_order.ticker = 'MY_ORDER_TICKER'

    update = {'event': 'rejected', 'order': rejected_order}
    test_positions_manager.update_position(update)

    assert 'MY_ORDER_TICKER' not in pending_orders


def test_update_position_deletes_pending_order_for_canceled(mocker, test_positions_manager):
    pending_orders = test_positions_manager._PositionsManager__pending_orders

    rejected_order = mocker.Mock()
    rejected_order.ticker = 'MY_ORDER_TICKER'

    update = {'event': 'canceled', 'order': rejected_order}
    test_positions_manager.update_position(update)

    assert 'MY_ORDER_TICKER' not in pending_orders


def test_open_position_exists_for_ticker_returns_true_correctly(test_positions_manager):
    assert test_positions_manager.open_position_exists_for_ticker('MY_TICKER')


def test_open_position_exists_for_ticker_returns_false_correctly(test_positions_manager):
    assert not test_positions_manager.open_position_exists_for_ticker('ANOTHER_TICKER')


def test_pending_order_exists_for_ticker_returns_true_correctly(test_positions_manager):
    assert test_positions_manager.pending_order_exists_for_ticker('MY_ORDER_TICKER')


def test_pending_order_exists_for_ticker_returns_false_correctly(test_positions_manager):
    assert not test_positions_manager.pending_order_exists_for_ticker('ANOTHER_ORDER_TICKER')


def test_ticker_is_busy_returns_true_if_position_is_open_for_ticker(test_positions_manager):
    assert test_positions_manager.ticker_is_busy('MY_TICKER')


def test_ticker_is_busy_returns_true_if_order_is_pending_for_ticker(test_positions_manager):
    assert test_positions_manager.ticker_is_busy('MY_ORDER_TICKER')


def test_ticker_is_busy_returns_false_if_ticker_is_free(test_positions_manager):
    assert not test_positions_manager.ticker_is_busy('FREE_TICKER')


def test_get_open_position_returns_correct_position(test_positions_manager):
    assert test_positions_manager.get_open_position_for_ticker('MY_TICKER') == 'mock_position'


def test_get_pending_order_for_ticker_returns_correct_order(test_positions_manager):
    assert test_positions_manager.get_pending_order_for_ticker('MY_ORDER_TICKER') == 'mock_order'


def test_get_pending_orders_returns_correct_orders(test_positions_manager):
    assert test_positions_manager.get_pending_orders() == {'MY_ORDER_TICKER': 'mock_order'}


def test_get_open_positions_for_strategy_gets_all_positions_for_strategy(mocker):
    mock_my_strategy_position_1 = mocker.Mock()
    mock_my_strategy_position_2 = mocker.Mock()
    mock_another_strategy_position = mocker.Mock()

    mock_my_strategy_position_1.strategy = 'MY_STRATEGY'
    mock_my_strategy_position_2.strategy = 'MY_STRATEGY'
    mock_another_strategy_position.strategy = 'ANOTHER_STRATEGY'

    open_positions = {
        'TK1': mock_my_strategy_position_1,
        'TK2': mock_my_strategy_position_2,
        'TK3': mock_another_strategy_position
    }
    expected_return = [mock_my_strategy_position_1, mock_my_strategy_position_2]

    manager = PositionsManager()
    manager._PositionsManager__open_positions = open_positions

    assert manager.get_open_positions_for_strategy('MY_STRATEGY') == expected_return


def test_open_position_opens_position(mocker, test_positions_manager):
    mock_position = mocker.Mock()
    mock_position.ticker = 'MY_ORDER_TICKER'
    test_positions_manager.open_position(mock_position)

    assert test_positions_manager._PositionsManager__open_positions['MY_ORDER_TICKER'] == mock_position


def test_close_position_closes_position(test_positions_manager):
    test_positions_manager.close_position('MY_TICKER')
    assert len(test_positions_manager._PositionsManager__open_positions) == 0


def test_close_position_raises_if_position_does_not_exist(test_positions_manager):
    with pytest.raises(Exception) as info:
        test_positions_manager.close_position('NOT_EXISTING_TICKER')

    assert str(info.value) == f'PositionsManager: No existing position for NOT_EXISTING_TICKER!'


def test_add_order_adds_order(mocker, test_positions_manager):
    mock_order = mocker.Mock()
    mock_order.ticker = 'NEW_TICKER'
    test_positions_manager.add_order(mock_order)

    assert test_positions_manager._PositionsManager__pending_orders['NEW_TICKER'] == mock_order


def test_add_order_raises_if_order_for_ticker(mocker, test_positions_manager):
    mock_order = mocker.Mock()
    mock_order.ticker = 'MY_ORDER_TICKER'

    with pytest.raises(Exception) as info:
        test_positions_manager.add_order(mock_order)

    assert str(info.value) == f'PositionsManager: Already pending order for {mock_order.ticker}!'


def test_delete_order_deletes_order(test_positions_manager):
    test_positions_manager.delete_order('MY_ORDER_TICKER')
    assert len(test_positions_manager._PositionsManager__pending_orders) == 0


def test_delete_pending_orders_raises_if_order_does_not_exist(test_positions_manager):
    with pytest.raises(Exception) as info:
        test_positions_manager.delete_order('NOT_EXISTING_TICKER')

    assert str(info.value) == f'PositionsManager: No pending order for NOT_EXISTING_TICKER!'