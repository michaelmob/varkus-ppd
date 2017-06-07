from datetime import date, datetime, timedelta
from decimal import Decimal as d
from django.core.management import call_command
from django.conf import settings
from django.test import TestCase
from conversions.models import Conversion
from .models import Invoice



class InvoiceTest(TestCase):
	"""
	Tests for Billing app.
	"""
	def create_random_tokens(self, widget):
		"""
		Helper function to create random tokens for a widget.
		"""
		call_command("randomtoken", widget.type, widget.id, chance=1, ip="74.125.157.99", quiet=True)
		call_command("randomtoken", widget.type, widget.id, chance=1, ip="74.125.65.91", quiet=True)
		call_command("randomtoken", widget.type, widget.id, chance=1, ip="173.231.140.219", quiet=True)


	def setUp(self):
		"""
		Setup test environment.
		"""
		from offers.tests import OfferTest
		from users.tests import UserTest
		from lockers.tests import LockerTest

		# Create offer and user
		self.offer = OfferTest.create_offer()
		self.user1 = UserTest.create_user("user1")
		self.user2 = UserTest.create_user("user2")

		# Set 'user1' to be referred by 'user2'
		# 'user2' should get a cut of 'user1' earnings
		self.user1.profile.referrer = self.user2
		self.user1.profile.save()

		# Modify user's party to have no minimum payout limit
		self.user1.profile.party.minimum_payout = 0.00
		self.user1.profile.party.save()

		# Create widget
		self.widget1 = LockerTest.create_widget(self.user1)
		self.widget2 = LockerTest.create_widget(self.user2)

		# Create token
		self.create_random_tokens(self.widget1)
		self.create_random_tokens(self.widget2)

		# Update conversions to be within billing period
		today = date.today()
		self.prev_month = datetime.today().replace(day=1) - timedelta(days=1)
		Conversion.objects.update(datetime=self.prev_month)


	def test_create(self):
		"""
		Test the creation of invoices.
		"""
		invoice = Invoice.objects.create_invoice(self.user1)
		self.assertIsNotNone(invoice)

		self.assertEqual(invoice.total_amount, d("18.00"))
		self.assertEqual(invoice.period_start_date.month, self.prev_month.month)
		self.assertEqual(invoice.period_end_date.month, self.prev_month.month)


	def test_create_with_referrals(self):
		"""
		Test the creation of an invoice when the user has referred others who
		have also gotten conversions.
		"""
		invoice = Invoice.objects.create_invoice(self.user2)
		self.assertIsNotNone(invoice)
		self.assertEqual(invoice.total_amount, d("19.80"))
		self.assertEqual(invoice.referral_amount, d("1.80"))


	def test_create_all(self):
		"""
		Test the creation of invoices for all users.
		"""
		self.assertGreater(Invoice.objects.create_all_invoices(), 1)
