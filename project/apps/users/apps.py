from django.apps import AppConfig



class UsersConfig(AppConfig):
	"""
	Configuration class for Users app.
	"""
	name = "users"


	def ready(self):
		"""
		Setup signals when ready.
		"""
		from . import signals