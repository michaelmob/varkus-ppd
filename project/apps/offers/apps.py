from django.apps import AppConfig



class OffersConfig(AppConfig):
	"""
	Configuration class for Offer app.
	"""
	name = "offers"


	def ready(self):
		"""
		Setup signals when ready.
		"""
		from . import signals