from django.conf import settings
from django.test import TestCase

from apps.user.tests import Test_User
from apps.lockers.tests import Test_Lockers


class Test_Token(TestCase):
	""" Tests for Token model """

	def test_create_random(self):
		pass


	def test_get(self):
		pass


	def test_get_or_create(self):
		pass


	def test_access(self):
		pass


	def test_clear(self):
		pass


class Test_Conversion(TestCase):
	""" Tests for Conversion model """

	def setUp(self):
		self.user = Test_User.create()


	def create(user):
		""" Not a test; create conversion for user """
		widget = Test_Lockers.create(user)
		token = Token.create_random(widget)
		return Conversion.get_or_create(token, datetime="TOKEN")[0]


	def test_time_to_complete(self):
		pass


	def test_get_or_create(self):
		pass