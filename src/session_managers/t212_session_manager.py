# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import requests
from bs4 import BeautifulSoup

import session_manager_base

class T212SessionManager(session_manager_base.SessionManagerBase):
	def __init__(self):
		self.__session = None
		self.__base_url = 'https://www.trading212.com/en/'

	def	__successfulResponse(self, response):
		return "\"isValid\":true" in response.text

	def login(self, username, password):
		self.__session = requests.Session()

		headers = {
			'user-agent':
				'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 '
				'(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
		}

		login_data = {
			'login[username]': username,
			'login[password]': password,
			'login[rememberMe]': 1
		}

		try:
			login_url = self.__base_url + 'login'
			login_page = self.__session.get(login_url, headers=headers)

			soup = BeautifulSoup(login_page.content, 'html.parser')

			login_data['login[_token]'] = soup.find('input', attrs={'name': 'login[_token]'})['value']
			authenticate_url = self.__base_url + 'authenticate'
			auth_page = self.__session.post(authenticate_url, data=login_data, headers=headers)

			return self.__successfulResponse(auth_page)
		except Exception:
			return False

	def getSession(self):
		return self.__session
