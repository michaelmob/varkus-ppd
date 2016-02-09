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
		user.earnings.add(30, 0.30)

		resp = self.client.post(
			reverse(signup),
			{
				# Personal
				"first_name": "tester",
				"last_name": "tester",
				"username": "username",
				
				# Account
				"email": "email@email.com",
				"password": "password",
				"confirm": "password",

				# Birthday
				"day": "1",
				"month": "1",
				"year": "1990"
			}
		)

		self.assertEqual(resp.status_code, 302)
		self.assertNotEqual(user.profile.party, None)