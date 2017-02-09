from django.apps import AppConfig



class TicketsConfig(AppConfig):
	"""
	Configuration class for Tickets app.
	"""
	name = "tickets"


	def ready(self):
		"""
		Setup signals when ready.
		"""
		from . import signals