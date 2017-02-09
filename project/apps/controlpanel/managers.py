from datetime import datetime, timedelta
from django.db import models



class BroadcastManager(models.Manager):
	"""
	Manager for Broadcast model.
	"""
	def create_broadcast(self, *args, **kwargs):
		"""
		Update current Broadcast if one already exists.
		"""
		broadcast = self.filter(**kwargs).first()

		if broadcast:
			broadcast.datetime = datetime.now()
			broadcast.readers.clear()
			broadcast.save()
			return broadcast

		return super(__class__, self).create(*args, **kwargs)



class NotificationManager(models.Manager):
	"""
	Manager for Notification model.
	"""
	def create_notification(self, *args, **kwargs):
		"""
		Update current Notification if one already exists.
		"""
		thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
		notification = self.filter(datetime__gt=thirty_minutes_ago, **kwargs).first()

		if notification:
			notification.datetime = datetime.now()
			notification.unread = True
			notification.save()
			return notification

		return super(__class__, self).create(*args, **kwargs)