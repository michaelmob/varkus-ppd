from datetime import datetime, timedelta
from decimal import Decimal
from django import test
from django.conf import settings
from django.utils.http import urlencode
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.management import call_command
from viking.utils import strings
from .models import Conversion, Token
from offers.models import Offer



class TokenTest(test.TestCase):
	"""
	Tests for Token model and manager.
	"""

	def setUp(self):
		"""
		Set up testing environment for TokenTest.
		"""
		from offers.tests import OfferTest
		from users.tests import UserTest
		from lockers.tests import LockerTest

		# Common
		self.ip_address = "173.53.243.198"
		self.user_agent = "Mozilla/5.0 Firefox"
		
		# Request
		self.request = test.RequestFactory().get(
			"/customer/details", 
			REMOTE_ADDR=self.ip_address,
			HTTP_USER_AGENT=self.user_agent
		)
		self.request.user = AnonymousUser()
		SessionMiddleware().process_request(self.request)
		self.request.session.save()

		# User and Object
		self.user = UserTest.create_user()
		self.widget = LockerTest.create_widget(self.user)

		# Token creation arguments
		self.create_args = (self.user, self.widget, self.ip_address, self.user_agent)

	
	def create_token(user, obj, ip_address, user_agent):
		"""
		Not a test; create testing token.
		"""
		return Token.objects.create(
			ip_address 	= ip_address,
			user 		= user,
			locker 		= obj,
			country 	= "US",
			unique 		= strings.random(64),
			user_agent 	= user_agent,
			session 	= None,
			datetime 	= datetime.now()
		)


	def test_get(self):
		"""
		Token should be able to be found by request's IP Address.
		"""
		self.__class__.create_token(*self.create_args)
		token = Token.objects.get_token(self.request, self.widget)

		self.assertIsNotNone(token)
		self.assertEqual(token.ip_address, self.ip_address)


	def test_get_or_create(self):
		"""
		Token is able to be fetched or created if it is non-existant.
		"""
		# Token_1 should be created
		token_1, created_1 = Token.objects.get_or_create_token(self.request, self.widget)

		# Token_2 should have been fetched and not created
		token_2, created_2 = Token.objects.get_or_create_token(self.request, self.widget)

		# Both tokens must exist
		self.assertIsNotNone(token_1)
		self.assertIsNotNone(token_2)

		# Assert that it was created and then fetched without being created
		self.assertTrue(created_1)
		self.assertFalse(created_2)


	def test_has_access(self):
		"""
		Test that token does not have 'access' to the locker object.
		"""
		token = __class__.create_token(*self.create_args)
		self.assertFalse(token.has_access())


	def test_create_random(self):
		"""
		Test for create_random() method.
		Specify IP address '173.1.1.1' because the offer we test created is a
		'US' offer.
		"""
		from lockers.tests import LockerTest
		from offers.tests import OfferTest

		widget = LockerTest.create_widget(self.user)
		offer = OfferTest.create_offer()
		
		call_command("randomtoken", widget.type, widget.id, chance=1, ip="173.1.1.1", quiet=True)

		token = Token.objects.first()
		self.assertIsNotNone(token)


	def test_clear(self):
		"""
		Test the clearing old tokens.
		"""
		token = self.__class__.create_token(*self.create_args)

		# Token should not be removed since it is not older than 30 days
		Token.objects.clear(30)
		self.assertEqual(Token.objects.count(), 1)

		# Set token older than 30 days
		token.datetime = datetime.now() - timedelta(days=60)
		token.save()

		# Token should be removed since it is older than 30 days
		Token.objects.clear(30)
		self.assertEqual(Token.objects.count(), 0)



class ConversionTest(test.TestCase):
	"""
	Tests for Conversion model and manager.
	"""

	def setUp(self):
		"""
		Set up testing environment.
		"""
		from offers.tests import OfferTest
		from users.tests import UserTest
		from lockers.tests import LockerTest

		# Common
		self.ip_address = "173.53.243.198"
		self.user_agent = "Mozilla/5.0 Firefox"
		self.referrer = UserTest.create_user("testee")
		self.offer = OfferTest.create_offer()
		self.user = UserTest.create_user(referrer=self.referrer)
		self.widget = LockerTest.create_widget(self.user)
		self.token = TokenTest.create_token(
			self.user, self.widget, self.ip_address, self.user_agent
		)
		self.cut_amount, self.referral_cut_amount = self.user.profile.get_cut_amounts()

		self.cut_amount = Decimal(self.cut_amount)
		self.referral_cut_amount = Decimal(self.referral_cut_amount)


	def refresh(self):
		"""
		Refresh object earnings.
		"""
		self.user.earnings.refresh_from_db()
		self.referrer.referralearnings.refresh_from_db()
		self.widget.earnings.refresh_from_db()
		self.offer.earnings.refresh_from_db()


	def test_get_or_create(self):
		"""
		get_or_create_conversion() make sure it really fetches or creates.
		"""
		conversion_1, created_1 = Conversion.objects.get_or_create_conversion(self.token)
		conversion_2, created_2 = Conversion.objects.get_or_create_conversion(self.token)

		self.assertTrue(created_1)
		self.assertFalse(created_2)


	def test_get_or_create_without_offer(self):
		"""
		get_or_create_conversion() conversion without offer.
		"""
		conversion, created = Conversion.objects.get_or_create_conversion(self.token)
		self.assertIsNotNone(conversion)
		self.assertEqual(conversion.payout, 0.00)


	def test_get_or_create_with_offer(self):
		"""
		get_or_create_conversion() conversion with offer.
		"""
		cut_amount = float(self.user.profile.get_cut_amounts()[0])
		conversion, created = Conversion.objects.get_or_create_conversion(self.token, self.offer)

		self.assertIsNotNone(conversion)
		self.assertEqual(
			float(conversion.payout), self.offer.payout - (self.offer.payout * cut_amount)
		)


	def test_signals_creating(self):
		"""
		Run tests on signals to see that correct values are being set to the
		created conversion.
		"""
		self.conversion, created = Conversion.objects.get_or_create_conversion(self.token, self.offer)
		self.conversion_total_payout = self.conversion.total_payout
		self.user_payout = Decimal(self.offer.payout) - (Decimal(self.offer.payout) * Decimal(self.cut_amount))
		self.referral_payout = self.conversion.payout * self.referral_cut_amount

		# Refresh earnings objects
		self.refresh()

		# Run assertions for user
		self.assertEqual(self.user.earnings.today, self.user_payout)
		self.assertEqual(self.widget.earnings.today, self.user_payout)
		self.assertEqual(self.offer.earnings.today, self.conversion_total_payout)

		# Assertion for referrer
		self.assertEqual(self.referrer.referralearnings.today, self.referral_payout)


	def test_signals_saving(self):
		"""
		Test that on a re-save the values remain the same as before, unless
		they shouldn't be the same.
		"""
		self.test_signals_creating()
		self.conversion.seconds = 0
		self.conversion.save()

		# Refresh earnings objects
		self.refresh()

		# Run user assertions
		self.assertEqual(self.user.earnings.today, self.user_payout)
		self.assertEqual(self.widget.earnings.today, self.user_payout)
		self.assertEqual(self.offer.earnings.today, self.conversion_total_payout)

		# Assertion for referrer
		self.assertEqual(self.referrer.referralearnings.today, self.referral_payout)


	def test_signals_deleting(self):
		"""
		Test that earnings are removed when Conversions are deleted.
		"""
		self.test_signals_creating()
		Conversion.objects.all().delete()

		# Refresh earnings objects
		self.refresh()

		# Run user assertions
		self.assertEqual(self.user.earnings.today, 0)
		self.assertEqual(self.widget.earnings.today, 0)
		self.assertEqual(self.offer.earnings.today, 0)

		# Assertion for referrer
		self.assertEqual(self.referrer.referralearnings.today, 0)



class TokenConversionIntegrationTest(test.TestCase):
	"""
	Tests for Webhooks.
	"""

	def url(self, **kwargs):
		"""
		Return webhook URL.
		"""
		return self.notify_url + urlencode(kwargs)


	def setUp(self):
		"""
		Setup scenario variables to test webhooks.
		"""			
		from offers.tests import OfferTest
		from users.tests import UserTest
		from lockers.tests import LockerTest

		# Create offer
		self.offer = OfferTest.create_offer()

		# Defaults
		self.ip_address = "173.53.243.198"
		self.password = settings.DEPOSITS[0][5]
		self.user_agent = "Mozilla/5.0 Firefox"
		self.notify_url = "/conversions/notify/%s/?" % self.password

		# User and Object
		self.user = UserTest.create_user()
		self.widget = LockerTest.create_widget(self.user)

		# Create token from above data
		self.token = TokenTest.create_token(
			self.user, self.widget, self.ip_address, self.user_agent
		)

		# Test Client
		self.client = test.Client(
			HTTP_USER_AGENT=self.user_agent, REMOTE_ADDR=self.ip_address
		)


	@test.override_settings(DEBUG=True)
	def test_webhook(self):
		"""
		Test webhook with all correct information.
		"""
		response = self.client.get(
			self.url(
				offer=self.offer.offer_id,
				payout=self.offer.payout,
				unique=self.token.unique,
				ip=self.ip_address,
				approved=1
			)
		)

		self.assertTrue(response.json()["success"])


	def test_webhook_with_invalid_offer(self):
		"""
		Test that webhook receiver will go through even if offer is invalid.
		"""
		response = self.client.get(
			self.url(
				offer=1000,
				payout=self.offer.payout,
				ip=self.ip_address,
				unique=self.token.unique,
				approved=1
			)
		)

		self.assertTrue(response.json()["success"])


	def test_webhook_and_validate_conversion(self):
		"""
		Send a notification and validate the data of the conversion after
		it has been accepted.
		"""
		self.test_webhook()

		obj = Conversion.objects.first()

		# Verify payout is correct
		total_payout = float(obj.total_payout)
		total_payout = total_payout - (total_payout * settings.DEFAULT_CUT_AMOUNT)
		self.assertEqual(float(obj.payout), total_payout)

		# Verify offer and offer name are correct
		self.assertEqual(obj.offer_name, obj.offer.name)