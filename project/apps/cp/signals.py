import json
from channels import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from apps.conversions.models import Conversion
from .models import Notification


@receiver(post_save, sender=Conversion)
def charts_conversion_signal(sender, instance, created, **kwargs):
	""" Signal for when a conversion is created, this signal clears cache for
	the charts """
	# Conversion must be being created and token must exist with a user
	if not (created and instance.offer and instance.user and not instance.blocked):
		return

	locker_ref = instance.locker.get_type() + "." + str(instance.locker.id)
	user_ref = instance.user.__class__.__name__.lower() + "." + str(instance.user.id)

	# cache.delete_many with memcached doesn't work
	cache_keys = (
		# User's Charts
		"line-chart-" + user_ref,
		"map-chart-" + user_ref,

		# User's Locker Charts
		"line-chart-" + locker_ref,
		"map-chart:." + locker_ref
	)

	cache.delete_many(cache_keys)


@receiver(post_save, sender=Notification)
def notification_signal(sender, instance, created, **kwargs):
	""" Signal for when a notification is created, this signal is responsible
		for publishing details of the notification to the redis queue that will,
		in turn, notify the user of their new notification """
	if not instance.user:
		return

	response = {
		"success": True,
		"message": "Notification",
		"type": "NOTIFICATION",
		"data": { }
	}

	Group("user-" + str(instance.user.pk)).send({
		"text": json.dumps(response)
	})