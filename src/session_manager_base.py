# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

class SessionManagerBase():
	def __init__(self, username, password):
		self.__username = username
		self.__password = password

	def login(self):
		raise NotImplementedError

	def logout(self):
		raise NotImplementedError
	