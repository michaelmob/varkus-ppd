import json
from channels import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from conversions.models import Conversion
from .models import Broadcast, Notification


@receiver(post_save, sender=Conversion)
def clear_chart_cache_signal(sender, instance, created, **kwargs):
	"""
	Activated when conversion is created.
	Clears cached charts.
	"""
	# Conversion must be being created and token must exist along with a user
	if not (created and instance.offer and instance.user and instance.is_blocked):
		return

	# User Reference
	user_ref = instance.user.__class__.__name__.lower() + "." + str(instance.user.id)
	keys = [
		# User's Charts
		"line-chart-" + user_ref,
		"map-chart-" + user_ref
	]

	# Locker Reference
	if instance.locker:
		locker_ref = instance.locker.type + "." + str(instance.locker.id)
		keys.append([
			# User's Locker Charts
			"line-chart-" + locker_ref,
			"map-chart-" + locker_ref
		])

	cache.delete_many(keys)


@receiver(post_save, sender=Broadcast)
def notify_broadcast_signal(sender, instance, created, **kwargs):
	"""
	Send user a notification that a Broadcast has been created.
	"""
	if not created:
		return

	if instance.is_staff:
		return

	response = {
		"success": True,
		"type": "BROADCAST"
	}

	Group("broadcast").send({
		"text": json.dumps(response)
	})


@receiver(post_save, sender=Notification)
def notify_notification_signal(sender, instance, created, **kwargs):
	"""
	Send user a notification that a Notification has been created.
	"""
	if not created:
		return

	response = {
		"success": True,
		"type": "NOTIFICATION"
	}

	Group("user-" + str(instance.recipient.pk)).send({
		"text": json.dumps(response)
	})