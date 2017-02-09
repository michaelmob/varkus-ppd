from django.test import TestCase, RequestFactory
from .models import Offer



class OfferTest(TestCase):
	"""
	Tests for Offers app.
	"""
	def create_offer(**kwargs):
		"""
		Not a test; create test offer
		"""
		creation_kwargs = {
			"offer_id": 500,
			"name":	"Name",
			"anchor": "Anchor",
			"requirements": "Requirements",
			"user_agent": "",
			"category": "Category",
			"countries": "US,UK,FR",
			"payout": 10.00,
			"earnings_per_click": 5.00,
			"tracking_url": "http://test.com/cl/1/50?s1="
		}

		creation_kwargs.update(kwargs)
		return Offer.objects.create(**creation_kwargs)


	def setUp(self):
		"""
		Setup testing environment.
		"""
		self.factory = RequestFactory()

		self.request = self.factory.get("/")
		self.request.META["REMOTE_ADDR"] = "173.54.24.123"
		self.request.META["HTTP_USER_AGENT"] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"

		# Offers
		OfferTest.create_offer(name="Unfindable", priority=True, countries="XX")
		OfferTest.create_offer(name="First")
		OfferTest.create_offer(name="Staff Priority", priority=True, payout=5)
		OfferTest.create_offer(name="User Blocked")
		OfferTest.create_offer(name="User Priority")
		OfferTest.create_offer(name="User Boosted")
		OfferTest.create_offer(name="Sixth")
		OfferTest.create_offer(name="Seventh")
		OfferTest.create_offer(name="Eight")
		OfferTest.create_offer(name="Ninth")

		from users.tests import UserTest
		from lockers.tests import LockerTest
		self.user = UserTest.create_user()
		self.widget = LockerTest.create_widget(self.user)


	def test_for_request(self):
		"""
		Test that chaining a `for_request` method to the queryset will limit
		the offers to relevant offers.
		"""
		# Invalid IP
		request2 = self.factory.get("/")
		request2.META["REMOTE_ADDR"] = "0.0.0.0"
		request2.META["HTTP_USER_AGENT"] = self.request.META["HTTP_USER_AGENT"]

		# Strange User-Agent
		request3 = self.factory.get("/")
		request3.META["REMOTE_ADDR"] = "173.54.24.123"
		request3.META["HTTP_USER_AGENT"] = "asdfosadjfojsad"

		# Empty User-Agent
		request4 = self.factory.get("/")
		request4.META["REMOTE_ADDR"] = "173.54.24.123"
		request4.META["HTTP_USER_AGENT"] = ""

		self.assertEqual(Offer.objects.all().for_request(self.request).count(), 9)
		self.assertEqual(Offer.objects.all().for_request(request2).count(), 0)
		self.assertEqual(Offer.objects.all().for_request(request3).count(), 9)
		self.assertEqual(Offer.objects.all().for_request(request4).count(), 9)


	def test_get_offers(self):
		"""
		Test that `get_offers` method on Offer's manager, returns offers.
		"""
		offer_count = len(Offer.objects.get_offers(self.request, self.widget))
		self.assertEqual(offer_count, 9)


	def test_get_offers_count(self):
		"""
		Test for `get_offers` method on Offer's manager, returns only 5 offers.
		"""
		offer_count = len(Offer.objects.get_offers(self.request, self.widget, 5))
		self.assertEqual(offer_count, 5)


	def test_get_offers_staff_priority_offers(self):
		"""
		Test that when using the `get_offers` method, the Staff prioritized offers
		are at the top.
		"""
		offers = Offer.objects.get_offers(self.request, self.widget)
		
		staff_offer = Offer.objects.filter(name="Staff Priority").first()
		unfindable_staff_offer = Offer.objects.filter(name="Unfindable").first()

		self.assertEqual(offers[0], staff_offer)
		self.assertNotEqual(offers[1], staff_offer)
		self.assertTrue(staff_offer in offers)
		self.assertFalse(unfindable_staff_offer in offers)


	def test_get_offers_user_blocked_staff_priority_offers(self):
		"""
		Test that when using the `get_offers` method, the Staff prioritized offers
		are blocked when a user specifically blocks them.
		"""
		staff_offer = Offer.objects.filter(name="Staff Priority").first()
		self.user.profile.offer_block.add(staff_offer)
		offers = Offer.objects.get_offers(self.request, self.widget)

		self.assertNotEqual(offers[0], staff_offer)
		self.assertFalse(staff_offer in offers)


	def test_get_offers_user_priority_offers(self):
		"""
		Test that user prioritized offers are listed at the top of the offers
		list but underneath staff picks.
		"""
		staff_offer = Offer.objects.filter(name="Staff Priority").first()
		user_offer = Offer.objects.filter(name="User Priority").first()
		self.user.profile.offer_priority.add(user_offer)
		offers = Offer.objects.get_offers(self.request, self.widget)

		self.assertEqual(offers[0], staff_offer)
		self.assertEqual(offers[1], user_offer)
		self.assertEqual(len(offers), 9)


	def test_get_offers_user_blocked_offers(self):
		"""
		Test that user blocked offers do not appear in the offers list.
		"""
		self.user.profile.offer_block.add(*list(Offer.objects.all()))
		offers = Offer.objects.get_offers(self.request, self.widget)
		
		self.assertEqual(len(offers), 0)