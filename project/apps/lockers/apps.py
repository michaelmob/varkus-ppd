from django.apps import AppConfig



class LockersConfig(AppConfig):
	"""
	Configuration class for the Lockers app and all her modules.
	"""
	name = "lockers"


	def ready(self):
		"""
		Setup signals when ready.
		"""
		from . import signals
		from modules.widgets import signals
		from modules.files import signals