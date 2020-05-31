# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

from trade_manager import TradeManager

def test_trade_open_positions_that_must_be_open(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_strategy = mocker.Mock()
    mock_order_to_open = mocker.Mock()

    mock_strategy_manager.get_strategies.return_value = [mock_strategy]
    mock_strategy.get_orders_to_be_opened.return_value = [mock_order_to_open]
    mock_strategy.get_name.return_value = "test_strategy"
    mock_order_to_open.ticker_symbol = "MKTKR"
    mock_trade_executor.submit_order.return_value = 42

    trade_manager = TradeManager(mock_trade_executor, mock_strategy_manager)
    trade_manager.trade()

    mock_strategy_manager.get_strategies.assert_called_once()
    mock_strategy.get_orders_to_be_opened.assert_called_once()
    mock_trade_executor.submit_order.assert_called_once_with(mock_order_to_open)
    assert "MKTKR" in trade_manager.opened_positions
    assert trade_manager.opened_positions["MKTKR"].strategy == "test_strategy"
    assert trade_manager.opened_positions["MKTKR"].order == mock_order_to_open
    assert trade_manager.opened_positions["MKTKR"].trade_id == 42

def test_trade_does_not_submit_order_if_ticker_already_busy(mocker):
    mock_trade_executor = mocker.Mock()
    mock_strategy_manager = mocker.Mock()
    mock_strategyA = mocker.Mock()
    mock_strategyB = mocker.Mock()
    mock_order_to_openA = mocker.Mock()
    mock_order_to_openB = mocker.Mock()

    mock_strategy_manager.get_strategies.return_value = [mock_strategyA, mock_strategyB]
    mock_strategyA.get_orders_to_be_opened.return_value = [mock_order_to_openA]
    mock_strategyB.get_orders_to_be_opened.return_value = [mock_order_to_openB]
    mock_order_to_openA.ticker_symbol = "MKTKR"
    mock_order_to_openB.ticker_symbol = "MKTKR"

    trade_manager = TradeManager(mock_trade_executor, mock_strategy_manager)
    trade_manager.trade()

    mock_strategyA.get_orders_to_be_opened.assert_called_once()
    mock_strategyB.get_orders_to_be_opened.assert_called_once()
    assert mock_trade_executor.submit_order.call_count == 1

# TODO: Add test for __close_positions() and __update_orders()
