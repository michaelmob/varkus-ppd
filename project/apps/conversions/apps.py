from django.apps import AppConfig



class ConversionsConfig(AppConfig):
	"""
	Configuration class for Offer app.
	"""
	name = "conversions"


	def ready(self):
		"""
		Setup signals when ready.
		"""
		from . import signals