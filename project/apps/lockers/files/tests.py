from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import manage
from .models import File

class Test(TestCase):
	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username="tester", email="tester@tester.com", password="tester")


	def test_upload(self):
		request = self.factory.post(
			"/files/process/",
			{
				"file": SimpleUploadedFile("gpa.txt", b"greatest_playa_alive")
			}
		)

		request.user = self.user
		response = manage.process(request)

		self.assertEqual(response.status_code, 200)