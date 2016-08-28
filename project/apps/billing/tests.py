from datetime import timedelta

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from apps.user.tests import Test_User
from apps.lockers.tests import Test_Lockers
from apps.conversions.models import Conversion, Token

from .models import Invoice


class Test_Invoice(TestCase):
	""" Tests for Billing app """

	def setUp(self):
		""" Setup test environment """
		self.user = Test_User.create()
		self.widget = Test_Lockers.create(self.user)
		self.token = Token.create_random(self.widget)

		# Amounts
		payout = 598.55
		self.user_payout = payout - (payout * settings.DEFAULT_CUT_AMOUNT)

		# Create conversion for user to reach minimum payout
		conversion = Conversion.get_or_create(token=self.token, payout=payout)[0]

		# Set conversion date to be within billing period
		conversion.datetime = conversion.datetime - timedelta(days=31)
		conversion.save()

		self.user = User.objects.get(pk=self.user.pk)


	def test_create(self):
		""" Create invoice """
		invoice = Invoice.create(self.user)
		
		self.assertIsNotNone(invoice)
		self.assertEquals(float(invoice.total_amount), self.user_payout)


	def test_create_all(self):
		""" Create invoices for all users """
		count = Invoice.create_all()
		self.assertGreater(count, 0)
