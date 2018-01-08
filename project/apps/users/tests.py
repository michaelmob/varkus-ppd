from datetime import date
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from .models import User, Party



class UserTest(TestCase):
	"""
	Tests for User model.
	"""

	def create_user(username="tester", referrer=None):
		"""
		Not a test; use in other tests to create user.
		"""
		user = User.objects.create_user(
			username=username,
			email="tester@tester.com",
			password="tester"
		)

		user.is_active = True
		user.first_name = "John"
		user.last_name = "Smith"
		user.save()

		if referrer:
			user.profile.referrer = referrer
		user.profile.birthday = date(1995, 5, 26)
		user.profile.save()
		return user


	def test_sign_up_has_group(self):
		"""
		Test for when a user is created, a party is automatically assigned
		to that user.
		"""
		user = UserTest.create_user()
		self.assertEqual(user.profile.party, Party.get_or_create_default())