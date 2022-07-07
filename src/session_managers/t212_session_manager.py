# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

import requests
from bs4 import BeautifulSoup

import websocket as ws
import base64
import random
import threading
import time
import copy

import session_manager_base

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    return error

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('42["subscribe","/ACCOUNT"]')
    ws.send('42["subscribe","/BUYERSSELLERS"]')
    ws.send('42["subscribe","/WORKING-SCHEDULES"]')

class T212SessionManager(session_manager_base.SessionManagerBase):
    def __init__(self):
        self.__session = None
        self.__websocket = None
        self.__base_url = 'https://www.trading212.com/en/'
        self.__websocket_url = 'wss://demo.trading212.com/streaming/events/?app=WC4&appVersion=5.111.4&EIO=3&transport=websocket'
        self.__headers = {
            'user-agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        self.__websocket_headers = {}

    def	__successful_response(self, response):
        return "\"isValid\":true" in response.text

    def __connect_websocket(self):
        dict_cookies = copy.deepcopy(self.__session.cookies.get_dict())
        str_cookies = "; ".join(["%s=%s" % (i, j) for i, j in dict_cookies.items()])

        self.__websocket_headers = copy.deepcopy(self.__headers)
        self.__websocket_headers['Sec-WebSocket-Key'] = str(
            base64.b64encode(bytes([random.randint(0, 255) for _ in range(16)])), 'ascii')
        self.__websocket_headers['Sec-WebSocket-Version'] = '13'
        self.__websocket_headers['Upgrade'] = 'websocket'

        self.__websocket = ws.WebSocketApp(
            self.__websocket_url,
            header=self.__websocket_headers,
            cookie=str_cookies,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close)

        websocket_thread = threading.Thread(target=self.__websocket.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()

        conn_timeout = 5
        while not self.__websocket.sock.connected and conn_timeout:
            time.sleep(1)
            conn_timeout -= 1

        return self.__websocket

    def login(self, username, password):
        self.__session = requests.Session()

        login_data = {
            'login[username]': username,
            'login[password]': password,
            'login[rememberMe]': 1
        }

        try:
            login_url = self.__base_url + 'login'
            authenticate_url = self.__base_url + 'authenticate'

            login_page = self.__session.get(login_url, headers=self.__headers)
            soup = BeautifulSoup(login_page.content, 'html.parser')

            login_data['login[_token]'] = \
                soup.find('input', attrs={'name': 'login[_token]'})['value']
            auth_page = \
                self.__session.post(authenticate_url, data=login_data, headers=self.__headers)

            self.__connect_websocket()

            return self.__successful_response(auth_page)
        except Exception:
            return False

    def logout(self):
        # self.__websocket.close()
        raise NotImplementedError

    def get_session(self):
        return self.__session

    def get_headers(self):
        return self.__headers

    def get_socket(self):
        return self.__websocket