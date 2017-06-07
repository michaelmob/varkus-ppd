import json
from django.test import TestCase, RequestFactory, Client
from users.tests import UserTest
from lockers.tests import LockerTest
from offers.tests import OfferTest
from conversions.models import Conversion, Token
from .views.webhooks import send_payload
from .models import WidgetVisitor



class WidgetTest(TestCase):
	"""
	Tests for the Widget module.
	"""
	def setUp(self):
		"""
		Set up testing environment.
		"""		
		self.ip_address = "173.52.23.243"
		self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36"

		self.client = Client(HTTP_USER_AGENT=self.user_agent, REMOTE_ADDR=self.ip_address)

		self.request = RequestFactory().get("/")
		self.request.session = self.client.session
		self.request.session.save()
		self.request.META["REMOTE_ADDR"] = self.ip_address
		self.request.META["HTTP_USER_AGENT"] = self.user_agent

		self.user = UserTest.create_user()
		self.widget = LockerTest.create_widget(self.user)
		self.offer = OfferTest.create_offer()
		self.token, self.created = Token.objects.get_or_create_token(
			self.request, self.widget, self.offer
		)


	def test_unlock_standalone(self):
		"""
		In standalone mode, the Widget should redirect the user to a link.
		"""
		self.widget.redirect_url = "http://google.com/"
		self.widget.save()

		self.token.unlocked = True
		self.token.save()

		response = self.client.get(self.widget.get_unlock_url())
		self.assertEqual(response["location"], self.widget.redirect_url)


	def test_unlock_pair(self):
		"""
		In paired mode, on unlock, the Widget should return the unlock view
		for the paired object.
		"""
		self.link = LockerTest.create_link("http://google.com/", self.user)
		self.widget.locker = self.link
		self.widget.save()

		self.token.unlocked = True
		self.token.save()

		response = self.client.get(self.widget.get_unlock_url())
		self.assertTrue(self.link.url in str(response.content))


	def test_new_user_add_visitor(self):
		"""
		Test that a visitor is added when a new user visits.
		"""
		self.widget.viral_mode = True
		self.widget.save()
		self.visitor_client = Client(HTTP_USER_AGENT=self.user_agent, REMOTE_ADDR="173.41.41.41")

		# Get URL and attempt to add visitor by visiting URL
		response = self.client.get(self.widget.get_locker_url())
		self.visitor_client.get(response.context_data["url"])

		# Assert that visitor count was updated
		visitor = WidgetVisitor.objects.order_by("-datetime").first()
		self.assertEquals(visitor.count, 1)


	def test_old_user_add_visitor(self):
		"""
		Test that a visitor is NOT added when an old user visits.
		"""
		self.widget.viral_mode = True
		self.widget.save()
		self.visitor_client = Client(HTTP_USER_AGENT=self.user_agent, REMOTE_ADDR="173.41.41.41")

		# Get URL
		response = self.client.get(self.widget.get_locker_url())

		# Visit many times
		for x in range(10):
			self.visitor_client.get(response.context_data["url"])

		# Assert that visitor count was updated
		visitor = WidgetVisitor.objects.order_by("-datetime").first()
		self.assertEquals(visitor.count, 1)


	def test_visitor_requirement_unsatisfied(self):
		"""
		Test that the locked view is blocking way to offers view if the visitor
		amount is not achieved.
		"""
		self.widget.viral_mode = True
		self.widget.viral_message = "TEST TEST TEST"
		self.widget.save()

		response = self.client.get(self.widget.get_locker_url())
		self.assertTrue("TEST TEST TEST" in str(response.content))


	def test_visitor_requirement_satisifed(self):
		"""
		Test for making sure that the unlock view comes up when the required
		visitor amount is achieved.
		"""
		self.widget.viral_mode = True
		self.widget.viral_count = 1
		self.widget.save()

		self.visitor_client = Client(HTTP_USER_AGENT=self.user_agent, REMOTE_ADDR="173.41.41.41")

		# Get URL
		response = self.client.get(self.widget.get_locker_url())
		
		# Add visitor
		self.visitor_client.get(response.context_data["url"])

		# Does the Offer wall appear?
		response = self.client.get(self.widget.get_locker_url())

		self.assertFalse("TEST TEST TEST" in str(response.content))
		self.assertTrue("/redirect/" in str(response.content))


	def test_webhook_sending_payload(self):
		"""
		Test that the webhook payload is sent.
		"""
		self.widget.webhook_url = (
			"https://httpbin.org/get?"
			"id={offer_id}&"
			"name={offer_name}&"
			"ip={ip}&"
			"ua={user_agent}&"
			"token={token}&"
			"widget={widget}&"
			"payout={payout}&"
			"approved={approved}&"
			"date={date}&"
			"time={time}&"
			"datetime={datetime}&"
			"rand={rand}&"
			"test={test}"
		)
		self.widget.save()

		conversion, created = Conversion.objects.get_or_create_conversion(self.token, self.offer)

		response = send_payload(conversion, True)
		response = json.loads(response)
		args = response["args"]

		self.assertEqual(args["id"], str(self.offer.pk))
		self.assertEqual(args["name"], str(self.offer.name))
		self.assertEqual(args["ip"], str(self.ip_address))
		self.assertEqual(args["ua"], str(self.user_agent))
		self.assertEqual(args["token"], str(self.token.unique))
		self.assertEqual(args["widget"], str(self.widget.code))
		self.assertEqual(args["payout"], str("%.2f" % conversion.payout))
		self.assertEqual(args["approved"], str(conversion.is_approved))
		self.assertEqual(args["test"], str(True))