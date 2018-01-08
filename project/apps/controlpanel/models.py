from datetime import datetime, timedelta
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from viking.utils.constants import BLANK_NULL
from .constants import ICON_CHOICES
from . import managers



class Broadcast(models.Model):
	"""
	Broadcast model for user notifications.
	"""
	objects		= managers.BroadcastManager()

	readers 	= models.ManyToManyField(User, blank=True)
	content 	= models.CharField(max_length=250)
	icon 		= models.CharField(max_length=20, choices=ICON_CHOICES)
	url 		= models.URLField(**BLANK_NULL)
	is_staff	= models.BooleanField(default=False)
	datetime 	= models.DateTimeField(auto_now_add=True)


	def get_broadcasts(user):
		"""
		Get broadcasts for a user.
		"""
		objects = (
			Broadcast.objects
				.filter(datetime__gte=datetime.now() - timedelta(days=7))
				.filter(**{"is_staff": False} if not user.is_staff else {})
				.order_by("-datetime")
		)

		return objects


	def get_broadcasts_with_unread(user):
		"""
		Get broadcasts for a user and also include an unread field.
		"""
		objects = __class__.get_broadcasts(user)
		zero_objects = True

		if len(objects) > 0:
			zero_objects = False
			unread_objects = [
				x[0] for x in 
					objects.exclude(readers__in=[user.pk])
						.only("id").values_list("id")
			]

		for object_ in objects:
			if zero_objects:
				object_.unread = False
			else:
				object_.unread = object_.pk in unread_objects

		return objects


	def get_unread_broadcasts(user):
		"""
		Returns unread broadcasts.
		"""
		return __class__.get_broadcasts(user).exclude(readers__in=[user.pk])


	def mark_as_read(user, queryset=None):
		"""
		Mark unread broadcasts as read.
		"""
		if not queryset:
			queryset = __class__.get_broadcasts(user)

		objects = queryset.exclude(readers__in=[user.pk])

		for object_ in objects:
			object_.readers.add(user)



class Notification(models.Model):
	"""
	Notification model for user notifications.
	"""
	objects 	= managers.NotificationManager()

	recipient 	= models.ForeignKey(User, on_delete=models.CASCADE, **BLANK_NULL)
	unread 		= models.BooleanField(default=True)
	content 	= models.CharField(max_length=250)
	icon 		= models.CharField(max_length=20, choices=ICON_CHOICES)
	url 		= models.URLField(**BLANK_NULL)
	datetime 	= models.DateTimeField(auto_now_add=True)


	def get_notifications(user):
		"""
		Get notifications for a user.
		"""
		week_ago = datetime.now() - timedelta(days=7)
		objects = (
			Notification.objects
				.filter(recipient=user)
				.filter(Q(datetime__gte=week_ago) | Q(unread=True))
				.order_by("-datetime")
		)

		return objects


	def get_unread_notifications(user):
		"""
		Returns unread notifications.
		"""
		return __class__.get_notifications(user).filter(unread=True)


	def mark_as_read(user):
		"""
		Mark unread notifications as read.
		"""
		Notification.objects.filter(unread=True).update(unread=False)