from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.user.tests import Test_User

from .models import Invoice


class Test_Billing(TestCase):
	user = None

	def setUp(self):
		self.user = Test_User.create()

	def test_auto_invoice(self):
		invoice = Invoice.create_auto(self.user)
		print(invoice.due_date)