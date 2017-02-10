from datetime import datetime, timedelta
from django import test
from .models import Broadcast, Notification



class BroadcastTest(test.TestCase):
	"""
	Tests for Broadcast model.
	"""
	def setUp(self):
		"""
		Setup testing environment.
		"""
		from users.tests import UserTest
		self.user = UserTest.create_user()


	def test_get_broadcasts(self):
		"""
		Test that getting broadcasts for a user works.
		"""
		Broadcast.objects.create(content="Broadcast", icon="success")
		objects = Broadcast.get_broadcasts(self.user)

		self.assertEqual(objects[0].content, "Broadcast")
		self.assertGreater(len(objects), 0)


	def test_get_broadcasts_staff(self):
		"""
		Test fetching a staff broadcast for a staff.
		"""
		self.user.is_staff = True

		Broadcast.objects.create(content="Broadcast", icon="success", is_staff=True)
		objects = Broadcast.get_broadcasts(self.user)

		self.assertEqual(objects[0].content, "Broadcast")
		self.assertGreater(len(objects), 0)



	def test_get_broadcasts_non_staff(self):
		"""
		Fetching broadcasts should not return Staff broadcasts for a user.
		"""
		# Staff
		Broadcast.objects.create(content="Broadcast", icon="success", is_staff=True)

		# Non staff
		Broadcast.objects.create(content="Broadcast", icon="success")

		objects = Broadcast.get_broadcasts(self.user)

		self.assertEqual(len(objects), 1)


	def test_get_broadcasts_old_broadcast(self):
		"""
		No broadcast older than 7 days should be shown.
		"""
		# Old
		Broadcast.objects.create(content="Broadcast", icon="success")
		Broadcast.objects.update(datetime=datetime.now() - timedelta(days=365))

		# New
		Broadcast.objects.create(content="Broadcast", icon="success")
		objects = Broadcast.get_broadcasts(self.user)

		self.assertEqual(len(objects), 1)


	def test_get_broadcasts_with_unread(self):
		"""
		Test that unread broadcasts gain the field 'unread'.
		"""
		bc1 = Broadcast.objects.create(content="Broadcast 1", icon="success")
		bc2 = Broadcast.objects.create(content="Broadcast 2", icon="success")
		bc2.readers.add(self.user)

		objects = Broadcast.get_broadcasts_with_unread(self.user)

		self.assertFalse(objects[0].unread)
		self.assertTrue(objects[1].unread)


	def test_get_unread_broadcasts(self):
		"""
		Test for valid count of unread broadcasts.
		"""
		Broadcast.objects.create(content="Broadcast", icon="success")
		count = Broadcast.get_unread_broadcasts(self.user).count()

		self.assertEqual(count, 1)


	def test_mark_as_read(self):
		"""
		Test that broadcasts are marked as read.
		"""
		Broadcast.objects.create(content="Broadcast", icon="success")
		Broadcast.mark_as_read(self.user)

		objects = Broadcast.get_broadcasts_with_unread(self.user)

		self.assertFalse(objects[0].unread)


	def test_identical_broadcasts(self):
		"""
		Test that identical broadcast datetimes are only updated.
		"""
		kwargs = {
			"content": "a", "icon": "b", "url": "c"
		}

		old_broadcast = Broadcast.objects.create_broadcast(**kwargs)
		new_broadcast = Broadcast.objects.create_broadcast(**kwargs)

		self.assertEqual(Broadcast.objects.count(), 1)



class NotificationTest(test.TestCase):
	"""
	Tests for Notification model.
	"""
	def setUp(self):
		"""
		Setup testing environment.
		"""
		from users.tests import UserTest
		self.user = UserTest.create_user()


	def test_get_notifications(self):
		"""
		Test that notifications can be fetched for a user.
		"""
		Notification.objects.create(recipient=self.user, content="Notification", icon="success")
		objects = Notification.get_notifications(self.user)

		self.assertEqual(objects[0].content, "Notification")
		self.assertGreater(len(objects), 0)


	def test_get_unread_notifications(self):
		"""
		Test unread notifications can be fetched.
		"""
		Notification.objects.create(recipient=self.user, content="Notification", icon="success")
		count = Notification.get_unread_notifications(self.user).count()

		self.assertEqual(count, 1)


	def test_mark_as_read(self):
		"""
		Test that notifications can be marked as read.
		"""
		Notification.objects.create(recipient=self.user, content="Notification 1", icon="success")
		Notification.mark_as_read(self.user)

		Notification.objects.create(recipient=self.user, content="Notification 2", icon="success")

		objects = Notification.get_notifications(self.user)

		self.assertFalse(Notification.objects.get(content="Notification 1").unread)
		self.assertTrue(Notification.objects.get(content="Notification 2").unread)


	def test_identical_notifications(self):
		"""
		Test that identical notification datetimes are only updated.
		"""
		kwargs = {
			"recipient": self.user, "content": "1", "icon": "2"
		}

		old_notification = Notification.objects.create_notification(**kwargs)
		old_notification.datetime = datetime.now() - timedelta(minutes=45)
		old_notification.save()

		# Should create another
		new_notification = Notification.objects.create_notification(**kwargs)
		self.assertEqual(Notification.objects.count(), 2)

		# Should NOT create a new one
		new_new_notification = Notification.objects.create_notification(**kwargs)
		new_new_notification.datetime = datetime.now() - timedelta(minutes=60)
		new_new_notification.save()
		self.assertEqual(Notification.objects.count(), 2)

		# But this one should as well
		new_new_notification = Notification.objects.create_notification(**kwargs)
		self.assertEqual(Notification.objects.count(), 3)