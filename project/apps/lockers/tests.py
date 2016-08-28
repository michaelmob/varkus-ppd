from django.conf import settings
from django.test import TestCase

from apps.user.tests import Test_User

from .widgets.models import Widget, Earnings


class Test_Lockers(TestCase):
	""" Tests for Lockers app """


	def create(user):
		""" Not a test; create test widget """
		obj, created = Widget.objects.get_or_create(
			user 		= user,
			name 		= "TEST",
			description	= "Widget for testing.",
			defaults = {
				"code": Widget().generate_code()
			}
		)
		Earnings.objects.get_or_create(obj=obj)
		return obj