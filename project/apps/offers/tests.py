from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from . import views
from .models import Offer


class Test(TestCase):

	def test_offers(self):
		print(
			Offer.get("173.69.12.31", "iPad")
		)
