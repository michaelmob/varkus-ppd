from django.apps import AppConfig



class SupportConfig(AppConfig):
	"""
	Configuration class for Support app.
	"""
	name = "support"


	def ready(self):
		"""
		Setup signals when ready.
		"""
		from . import signals