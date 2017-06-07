from django.test import TestCase, Client, override_settings
from django.shortcuts import reverse



class LockerIntegrationTest(TestCase):
	"""
	Integration tests for Locker objects.
	"""
	def setUp(self):
		"""
		Setup testing environment.
		"""
		# Create offer
		from offers.tests import OfferTest
		from users.tests import UserTest
		from lockers.tests import LockerTest
		self.offer = OfferTest.create_offer()
		self.user = UserTest.create_user()
		self.widget = LockerTest.create_widget(self.user)
		self.widget.redirect_url = "http://google.com/"
		self.widget.save()
		self.client = Client(
			HTTP_USER_AGENT="Mozilla/5.0 Firefox", REMOTE_ADDR="173.53.243.198"
		)


	@override_settings(DEBUG=False)
	def test_visit_offers_wall(self):
		"""
		Test that the offer wall does not produce an error.
		"""
		response = self.client.get(self.widget.get_locker_url())
		self.assertContains(response, "Anchor")


	def test_token_creation_on_offer_redirect(self):
		"""
		Test that token is created when a user clicks an offer.
		"""
		self.client.get(self.offer.get_redirect_url(self.widget))
		
		from conversions.models import Token
		self.assertIsNotNone(Token.objects.filter(locker_id=self.widget.id).first())


	def test_unlock_without_conversion(self):
		"""
		Test that a user cannot access the unlock page when they have not
		completed an offer
		"""
		response = self.client.get(self.widget.get_unlock_url())
		self.assertEqual(response["location"], self.widget.get_locker_url())


	def test_unlock_with_conversion(self):
		"""
		Test that object is unlocked when a user has their Conversion.
		"""
		from conversions.models import Conversion, Token

		# Create Token
		self.client.get(self.offer.get_redirect_url(self.widget))

		# Create Conversion
		token = Token.objects.filter(locker_id=self.widget.id).first()
		token.unlocked = True
		token.save()

		# Create Token
		response = self.client.get(self.widget.get_unlock_url())
		self.assertEqual(response["location"], self.widget.redirect_url)