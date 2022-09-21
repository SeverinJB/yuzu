# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest
import pandas as pd
from asyncmock import AsyncMock

from trades_manager import TradesManager
from trade_objects import Order, Position, Signal


# TODO: Add test for __outofmarket
# TODO: Add test for __exit_positions
# TODO: Add test for __enter_positions
# TODO: Add test for __classify_signals
# TODO: Add test for __collect_trade_signals
# TODO: Clean up test (refactor code duplication)


@pytest.fixture
def mock_trade_objects():
    ticker = 'MY_TICKER'

    mock_order = Order('MOCK_STRATEGY', ticker, '', '', '')
    mock_order.id = ''
    mock_order.valid_for_seconds = '120'
    mock_order.submitted_at = pd.Timestamp('2022-09-16 16:53:00+00:00')

    mock_signal = Signal(mock_order, True)

    mock_position = Position('MOCK_STRATEGY', ticker, '', '', '')

    mock_strategy = AsyncMock()
    mock_strategy.get_trade_signals = AsyncMock(return_value=[mock_signal])

    return mock_order, mock_signal, mock_position


@pytest.fixture
def mock_strategy(mock_trade_objects):
    _, mock_signal, _ = mock_trade_objects

    mock_strategy = AsyncMock()
    mock_strategy.get_trade_signals = AsyncMock(return_value=[mock_signal])

    return mock_strategy


@pytest.fixture
def mock_strategies_manager(mocker, mock_strategy):
    mock_strategies_manager = mocker.Mock()
    mock_strategies_manager.get_strategies.return_value = {'MOCK_STRATEGY': mock_strategy}

    return mock_strategies_manager


@pytest.fixture
def mock_positions_manager(mocker, mock_trade_objects):
    mock_order, _, mock_position = mock_trade_objects
    mock_positions_manager = mocker.Mock()
    mock_positions_manager.get_open_position_for_ticker.return_value = mock_position
    mock_positions_manager.get_pending_orders.return_value = {'TICKER': mock_order}

    return mock_positions_manager


@pytest.fixture
def test_trade_executor(mocker):
    mock_trade_executor = mocker.Mock()
    mock_trade_executor.close_position.return_value = True
    mock_trade_executor.submit_order = AsyncMock(return_value=None)
    mock_trade_executor.cancel_order = AsyncMock(return_value=200)
    mock_trade_executor.get_latest_order_updates.return_value = ['list', 'updates']

    return mock_trade_executor


@pytest.fixture
def test_trades_manager(test_trade_executor, mock_strategies_manager, mock_positions_manager):
    trades_manager = TradesManager(test_trade_executor,
                                   mock_strategies_manager,
                                   mock_positions_manager)

    return trades_manager


@pytest.mark.asyncio
async def test_time_out_pending_orders_returns_none_for_cancelled_order(test_trades_manager):
    assert await test_trades_manager._TradesManager__time_out_pending_orders() is None


@pytest.mark.asyncio
async def test_time_out_pending_orders_raises_if_order_not_cancelled(test_trades_manager):
    executor = test_trades_manager._TradesManager__trade_executor
    executor.cancel_order = AsyncMock(return_value=400)

    with pytest.raises(Exception) as info:
        await test_trades_manager._TradesManager__time_out_pending_orders()

    assert str(info.value) == f'TradesManager: Order was not cancelled correctly, 400'


def test_check_for_order_updates_calls_function_update_position(test_trades_manager):
    test_trades_manager._TradesManager__check_for_order_updates()
    positions_manager = test_trades_manager._TradesManager__positions_manager

    positions_manager.update_position.assert_called()


@pytest.mark.asyncio
async def test_collect_trade_signals_returns_signals_list(test_trades_manager, mock_trade_objects):
    _, mock_signal, _ = mock_trade_objects
    assert await test_trades_manager._TradesManager__collect_trade_signals() == [mock_signal]


@pytest.mark.asyncio
async def test_collect_trade_signals_returns_empty_list_if_none(test_trades_manager, mock_strategy):
    mock_strategy.get_trade_signals = AsyncMock(return_value=None)
    assert await test_trades_manager._TradesManager__collect_trade_signals() == []


@pytest.mark.asyncio
async def test_close_positions_tries_to_close_open_position_on_exit_signal(mocker, test_instances):
    trades_manager, trade_executor, positions_manager, strategies_manager, strategy, signal \
        = test_instances
    ticker = 'MY_TICKER'

    await trades_manager.trade()

    strategies_manager.get_strategies.assert_called_once()
    strategy.get_trade_signals.assert_called()
    # positions_manager.open_position_exists_for_ticker.assert_called_once_with(ticker)
    # positions_manager.get_open_position_for_ticker.assert_called_once_with(ticker)
    # trade_executor.close_position.assert_called_once_with(trade_id)
    # positions_manager.close_position.assert_called_once_with(ticker)


def test_close_does_not_do_anything_if_no_position_for_signal_is_open(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategies_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    ticker = 'TICKER'
    mock_strategy = mocker.Mock()
    mock_strategy.get_exit_signals.return_value = [ticker]
    mock_strategies_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.open_position_exists_for_ticker.return_value = False

    manager = TradesManager(
        mock_trade_executor, mock_strategies_manager, mock_positions_manager)
    # mocker.patch('trade_manager.TradeManager._TradeManager__open_positions')
    manager.trade()

    mock_strategies_manager.get_strategies.assert_called_once()
    mock_strategy.get_exit_signals.assert_called_once()
    mock_positions_manager.open_position_exists_for_ticker.assert_called_once_with(ticker)

    mock_positions_manager.get_open_position_for_ticker.assert_not_called()
    mock_trade_executor.close_position.assert_not_called()
    mock_positions_manager.close_position.assert_not_called()


def test_close_positions_raises_if_executor_fails_to_close_position(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    ticker = 'TICKER'
    trade_id = 42
    mock_strategy = mocker.Mock()
    mock_strategy.get_exit_signals.return_value = [ticker]
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.open_position_exists_for_ticker.return_value = True
    mock_positions_manager.get_open_position_for_ticker.return_value = Position('', '', trade_id)
    mock_trade_executor.close_position.return_value = False

    manager = TradesManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__open_positions')
    with pytest.raises(Exception):
        manager.trade()
    mock_positions_manager.close_position.assert_not_called()


def test_opene_positions_tries_to_open_position_on_entry_signal(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    ticker = 'TICKER'
    trade_id = 1
    strategy_name = 'StrategyA'
    mock_strategy = mocker.Mock()
    mock_order = mocker.Mock()
    mock_order.ticker = ticker
    mock_order.id = trade_id
    mock_order_response = mocker.Mock()
    mock_order_response.id = trade_id
    mock_order_response.order = 'mock_executed_order'

    mock_strategy.get_entry_signals.return_value = [mock_order]
    mock_strategy.get_name.return_value = strategy_name
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.ticker_is_busy.return_value = False
    mock_trade_executor.submit_order.return_value = mock_order_response

    manager = TradesManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__close_positions')
    manager.trade()

    mock_strategy_manager.get_strategies.assert_called_once()
    mock_strategy.get_entry_signals.assert_called_once()
    mock_positions_manager.ticker_is_busy.assert_called_once_with(ticker)
    mock_trade_executor.submit_order.assert_called_once_with(mock_order)
    mock_positions_manager.open_position.assert_called_once_with(
        Position(strategy_name, mock_order_response.order, mock_order_response.id))


def test_open_positions_does_nothing_if_ticker_already_busy(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    ticker = 'TICKER'
    mock_strategy = mocker.Mock()
    mock_order = mocker.Mock()
    mock_order.ticker = ticker

    mock_strategy.get_entry_signals.return_value = [mock_order]
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.ticker_is_busy.return_value = True

    manager = TradesManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__close_positions')
    manager.trade()

    mock_strategy_manager.get_strategies.assert_called_once()
    mock_strategy.get_entry_signals.assert_called_once()
    mock_positions_manager.ticker_is_busy.assert_called_once_with(ticker)
    mock_trade_executor.submit_order.assert_not_called()
    mock_positions_manager.open_position.assert_not_called()


def test_open_positions_raise_exception_if_executor_fails_to_open_position(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    mock_strategy = mocker.Mock()
    mock_order = mocker.Mock()

    mock_strategy.get_entry_signals.return_value = [mock_order]
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.ticker_is_busy.return_value = False
    mock_trade_executor.submit_order.return_value = None

    manager = TradesManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    # mocker.patch('trade_manager.TradeManager._TradeManager__close_positions')
    with pytest.raises(Exception):
        manager.trade()
    mock_positions_manager.open_position.assert_not_called()
