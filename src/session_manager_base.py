# Copyright Yuzu 2022
# Any unauthorised usage forbidden

class SessionManagerBase():
	def login(self, username, password):
		raise NotImplementedError

	def logout(self):
		raise NotImplementedError
