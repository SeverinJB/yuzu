# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import pytest

import requests

from session_managers.t212_session_manager import T212SessionManager as Manager

class MockLoginPage:
    def __init__(self):
        self.content = 'mock_content'

def test_login_returns_true_on_successful_login(mocker):
    username = 'test_username'
    password = 'test_password'
    mock_login_token = 'mock_token'
    login_data = {
        'login[username]': username,
        'login[password]': password,
        'login[rememberMe]': 1,
        'login[_token]' : mock_login_token
    }
    headers = {
        'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    login_url = 'https://www.trading212.com/en/login'
    authenticate_url = 'https://www.trading212.com/en/authenticate'
    mock_auth_response = "... \"isValid\":true ..."

    mocked_session_class = mocker.patch('requests.Session')
    mocked_session = mocked_session_class.return_value
    mocked_session.get.return_value = MockLoginPage()
    mocked_session.post.return_value.text = mock_auth_response

    mocked_bs4_class = mocker.patch('session_managers.t212_session_manager.BeautifulSoup')
    mocked_soup = mocked_bs4_class.return_value
    mocked_soup.find.return_value = {'value' : mock_login_token}

    manager = Manager()
    assert manager.login(username, password)
    mocked_session.get.assert_called_once_with(login_url, headers=headers)
    mocked_soup.find.assert_called_once_with('input', attrs={'name': 'login[_token]'})
    mocked_session.post.assert_called_once_with(authenticate_url, data=login_data, headers=headers)

def test_login_sets_session_correctly(mocker):
    mocker.patch('requests.Session')
    mock_session_value = 'MockSessionValue'
    requests.Session.return_value = mock_session_value

    manager = Manager()
    manager.login('username', 'password')

    assert manager.get_session() == mock_session_value

def test_get_headers_returns_headers(mocker):
    expected_headers = {
            'user-agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }

    manager = Manager()
    assert manager.get_headers() == expected_headers

def test_login_successfully_logs_in():
    correct_username = "tradingyuzu@gmail.com"
    correct_password = "212TradingYuzu2020"

    manager = Manager()
    assert manager.login(correct_username, correct_password)

def test_login_returns_false_on_unsuccessful_login(mocker):
    username = 'wrong_username'
    password = 'wrong_password'

    mock_auth_response = "... \"isValid\":false ..."

    mocked_session_class = mocker.patch('requests.Session')
    mocked_session = mocked_session_class.return_value
    mocked_session.get.return_value = MockLoginPage()
    mocked_session.post.return_value.text = mock_auth_response

    mocked_bs4_class = mocker.patch('session_managers.t212_session_manager.BeautifulSoup')
    mocked_soup = mocked_bs4_class.return_value
    mocked_soup.find.return_value = {'value' : 'mock_token'}

    manager = Manager()
    assert not manager.login(username, password)
