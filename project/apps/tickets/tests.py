import os.path
from django import test
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from users.tests import UserTest
from .models import Thread, Post
from .forms import ThreadForm, PostForm



class ThreadTest(test.TestCase):
	"""
	Tests for ticket Thread model.
	"""
	def create_thread(user):
		"""
		Not a test; Create Thread for testing purposes.
		"""
		data = {
			"subject": "Test Subject",
			"category": "OTHER",
			"priority": "5",
			"message": "This is a test message. This must be over 20 characters long."
		}

		form = ThreadForm(data, {"file": SimpleUploadedFile("test.txt", b"x")})
		instance = form.save(commit=False)
		instance.user = user
		return form


	def setUp(self):
		"""
		Set up testing environment for ThreadTest.
		"""
		self.user = UserTest.create_user()
		self.form = ThreadTest.create_thread(self.user)


	def tearDown(self):
		"""
		Deconstruct testing environment.
		"""
		Post.objects.all().delete()

	
	def test_thread_form(self):
		"""
		Test that Thread form creates a new thread on save.
		"""
		self.assertTrue(self.form.is_valid())
		self.assertIsNotNone(self.form.save())
		self.assertTrue(Thread.objects.exists())

		
	def test_post_is_created(self):
		"""
		On Thread form save, a post should be created.
		"""
		self.form.save()
		self.assertTrue(Post.objects.exists())



class PostTest(test.TestCase):
	"""
	Tests for ticket Post model.
	"""
	def create_post(user, thread):
		"""
		Not a test; Create Post for testing purposes.
		"""
		data = {
			"message": "This is a test message. This must be over 20 characters long."
		}

		form = PostForm(data, {"file": SimpleUploadedFile("test.txt", b"x")})
		instance = form.save(commit=False)
		instance.user = user
		instance.thread = thread
		return form


	def setUp(self):
		"""
		Set up testing environment for ThreadTest.
		"""
		self.user = UserTest.create_user()
		self.thread = ThreadTest.create_thread(self.user).save()
		self.form = PostTest.create_post(self.user, self.thread)


	def tearDown(self):
		"""
		Deconstruct testing environment.
		"""
		Post.objects.all().delete()

	
	def test_post_form(self):
		"""
		Test that Post form creates a post for a thread.
		"""
		self.assertTrue(self.form.is_valid())
		self.assertIsNotNone(self.form.save())
		self.assertTrue(Post.objects.exists())

		
	def test_unread_toggled(self):
		"""
		Test for when posting, the unread toggle is flipped by the signal.
		"""
		self.form.save()

		staff_user = UserTest.create_user(username="staff_user")
		staff_user.is_staff = True
		staff_user.save()

		PostTest.create_post(staff_user, self.thread).save()
		self.thread.refresh_from_db()

		self.assertTrue(self.thread.unread)



	def test_file_is_deleted(self):
		"""
		Test when post is deleted, the file is also deleted.
		"""
		post = Post.objects.get(pk=1)
		file_name = os.path.join("media", post.file.name)

		self.assertTrue(os.path.isfile(file_name))
		post.delete()
		self.assertFalse(os.path.isfile(file_name))