# Copyright Burg&Biondi 2020
# Any unauthorized usage forbidden

class SessionManagerBase():
	def login(self, username, password):
		raise NotImplementedError

	def logout(self):
		raise NotImplementedError
