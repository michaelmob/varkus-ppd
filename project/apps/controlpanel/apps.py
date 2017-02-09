from django.apps import AppConfig


class ControlPanelConfig(AppConfig):
	"""
	Configuration class for the Control Panel app.
	"""
	name = "controlpanel"
	verbose_name = "Control Panel"


	def ready(self):
		"""
		Setup signals when ready.
		"""
		from . import signals