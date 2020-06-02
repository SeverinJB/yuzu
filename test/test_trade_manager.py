# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

from trade_manager import TradeManager
from positions_manager import Position

# TODO: Add test for __update_orders()
# TODO: Clean up test (refactor code duplication)

def test_close_positions_tries_to_close_open_position_on_exit_signal(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    ticker = 'TICKER'
    trade_id = 42
    mock_strategy = mocker.Mock()
    mock_strategy.get_exit_signals.return_value = [ticker]
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.open_position_exists_for_ticker.return_value = True
    mock_positions_manager.get_open_position.return_value = Position('', '', trade_id)
    mock_trade_executor.close_position.return_value = True

    manager = TradeManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__open_positions')
    manager.trade()

    mock_strategy_manager.get_strategies.assert_called_once()
    mock_strategy.get_exit_signals.assert_called_once()
    mock_positions_manager.open_position_exists_for_ticker.assert_called_once_with(ticker)
    mock_positions_manager.get_open_position.assert_called_once_with(ticker)
    mock_trade_executor.close_position.assert_called_once_with(trade_id)
    mock_positions_manager.close_position.assert_called_once_with(ticker)

def test_close_does_not_do_anything_if_no_position_for_signal_is_open(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    ticker = 'TICKER'
    mock_strategy = mocker.Mock()
    mock_strategy.get_exit_signals.return_value = [ticker]
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.open_position_exists_for_ticker.return_value = False

    manager = TradeManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__open_positions')
    manager.trade()

    mock_strategy_manager.get_strategies.assert_called_once()
    mock_strategy.get_exit_signals.assert_called_once()
    mock_positions_manager.open_position_exists_for_ticker.assert_called_once_with(ticker)

    mock_positions_manager.get_open_position.assert_not_called()
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
    mock_positions_manager.get_open_position.return_value = Position('', '', trade_id)
    mock_trade_executor.close_position.return_value = False

    manager = TradeManager(
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
    mock_order.ticker_symbol = ticker
    mock_order.id = trade_id
    mock_order_response = mocker.Mock()
    mock_order_response.id = trade_id
    mock_order_response.order = 'mock_executed_order'

    mock_strategy.get_entry_signals.return_value = [mock_order]
    mock_strategy.get_name.return_value = strategy_name
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.ticker_is_busy.return_value = False
    mock_trade_executor.submit_order.return_value = mock_order_response

    manager = TradeManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__close_positions')
    manager.trade()

    mock_strategy_manager.get_strategies.assert_called_once()
    mock_strategy.get_entry_signals.assert_called_once()
    mock_positions_manager.ticker_is_busy.assert_called_once_with(ticker)
    mock_trade_executor.submit_order.assert_called_once_with(mock_order)
    mock_positions_manager.open_position.assert_called_once_with(
        Position(strategy_name, mock_order_response.order, mock_order_response.id))

def test_opene_positions_does_nothing_if_ticker_already_busy(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    ticker = 'TICKER'
    mock_strategy = mocker.Mock()
    mock_order = mocker.Mock()
    mock_order.ticker_symbol = ticker

    mock_strategy.get_entry_signals.return_value = [mock_order]
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.ticker_is_busy.return_value = True

    manager = TradeManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__close_positions')
    manager.trade()

    mock_strategy_manager.get_strategies.assert_called_once()
    mock_strategy.get_entry_signals.assert_called_once()
    mock_positions_manager.ticker_is_busy.assert_called_once_with(ticker)
    mock_trade_executor.submit_order.assert_not_called()
    mock_positions_manager.open_position.assert_not_called()

def test_opene_positions_raise_exception_if_executor_fails_to_open_position(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_positions_manager = mocker.Mock()

    mock_strategy = mocker.Mock()
    mock_order = mocker.Mock()

    mock_strategy.get_entry_signals.return_value = [mock_order]
    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_positions_manager.ticker_is_busy.return_value = False
    mock_trade_executor.submit_order.return_value = None

    manager = TradeManager(
        mock_trade_executor, mock_strategy_manager, mock_positions_manager)
    mocker.patch('trade_manager.TradeManager._TradeManager__close_positions')
    with pytest.raises(Exception):
        manager.trade()
    mock_positions_manager.open_position.assert_not_called()
