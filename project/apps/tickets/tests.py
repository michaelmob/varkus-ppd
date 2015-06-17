from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from . import views
from .models import Thread, Post

class Test(TestCase):
	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username="tester", email="tester@tester.com", password="tester")


	def test_create_thread_no_image(self):
		# Create Thread
		request = self.factory.post(
			"/tickets/",
			{
				"subject": "Test Ticket without Image",
				"type": "help",
				"priority": "1",
				"message": "This is a test ticket. It must be over 20 characters.",
				"image": None
			}
		)

		# Messages Middleware
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)

		request.user = self.user
		response = views.list(request)

		self.assertIsNotNone(Thread.objects.get(pk=1))
		self.assertEqual(response.status_code, 302)
