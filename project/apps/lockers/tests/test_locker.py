from django.test import TestCase
from modules.widgets.models import Widget
from modules.links.models import Link



class LockerTest(TestCase):
	"""
	Tests for Lockers app.
	"""
	def create_widget(user):
		"""
		Not a test; create test widget.
		"""
		obj, created = Widget.objects.get_or_create(
			user 		= user,
			name 		= "TEST",
			description	= "Widget for testing.",
			defaults = {
				"code": Widget.generate_code()
			}
		)
		Widget.get_earnings_model().objects.get_or_create(parent=obj)
		return obj


	def create_link(url, user):
		"""
		Not a test; create test link.
		"""
		obj, created = Link.objects.get_or_create(
			user 		= user,
			url 		= url,
			name 		= "TEST",
			description	= "Link for testing.",
			defaults = {
				"code": Link.generate_code()
			}
		)
		Link.get_earnings_model().objects.get_or_create(parent=obj)
		return obj