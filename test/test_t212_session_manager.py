# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

from session_managers.t212_session_manager import T212SessionManager as Manager

correct_username = "tradingyuzu@gmail.com"
correct_password = "212TradingYuzu2020"

def test_login_returns_true_on_successful_login_and_sets_session():
	manager = Manager()

	assert manager.getSession() is None
	assert manager.login(correct_username, correct_password)
	assert manager.getSession() is not None
	# TODO: Test that we are actually logged-in


# def test_login_return_false_on_unsuccessful_login():
# 	username = "wrong_username"
# 	password = "wrong_password"
#
# 	manager = Manager()
# 	assert not manager.login(username, password)

