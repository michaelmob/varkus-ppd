from datetime import date

from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from .views import signup
from .models import User, Party


class Test_User(TestCase):
	# Not a test by itself, use in other tests to
	# create user
	def create():
		Party.initiate()

		user = User.objects.create_user(username="tester", email="tester@tester.com", password="tester")
		user.is_active = True
		user.first_name = "John"
		user.last_name = "Smith"
		user.save()

		user.profile.party = Party.default()
		user.profile.birthday = date(1995, 5, 26)
		user.profile.save()
		return user


	def test_sign_up(self):
		user = Test_User.create()
		self.assertEqual(user.profile.party, Party.default())