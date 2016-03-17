import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from .models import Conversion, Token
from utils.dicts import keep_wanted
from apps.lockers.fields import locker_ref_to_object


@receiver(post_save, sender=Token)
def unlock_signal(sender, instance, created, **kwargs):
	""" Signal for after a token is saved, this signal is responsible
		for publishing details of the locker to the redis queue but only if
		the token is marked as accessible (meaning the user has access to the
		locker that is attached) """
	if not (instance.locker and instance.session and instance.access()):
		return

	# Sometimes instance.locker is the reference, and sometimes it's the object
	if isinstance(instance.locker, str):
		instance.locker = locker_ref_to_object(instance.locker)
		
		if not instance.locker:
			return

	# Send response to Locker
	response = {
		"success": True,
		"message": "Unlocked " + instance.locker.get_type().title(),
		"data": {
			"locker": instance.locker.get_type(),
			"code": instance.locker.code,
			"url": instance.locker.get_unlock_url()
		}
	}

	locker = RedisPublisher(facility="locker", sessions=[instance.session])
	locker.publish_message(RedisMessage(json.dumps(response)))


@receiver(post_save, sender=Token)
def notify_click_signal(sender, instance, created, **kwargs):
	""" Signal for when a token is created, this signal is responsible
		for publishing details of the token to the redis queue that will,
		in turn, notify the user a click has went through """
	if not (created and instance.user):
		return

	earnings = instance.user.earnings

	response = {
		"success": True,
		"message": "Click",
		"type": "TOKEN",
		"data": {
			"user": {
				"clicks": earnings.clicks + 1,
				"clicks_today": earnings.clicks_today + 1
			}
		}
	}

	redis_publisher = RedisPublisher(facility="cp", users=[instance.user.username])
	redis_publisher.publish_message(RedisMessage(json.dumps(response)), expire=0)


@receiver(post_save, sender=Conversion)
def notify_conversion_signal(sender, instance, created, **kwargs):
	""" Signal for when a conversion is created, this signal is responsible
		for publishing details of the conversion to the redis queue that will,
		in turn, notify the user a conversion has went through """
	if not (created and instance.user and not instance.blocked):
		return

	# Add wanted data to conversion_data
	conversion_data = keep_wanted(instance, (
		"user_payout", "referral_payout", "approved"))

	# Keep wanted user data
	user_data = keep_wanted(User.objects.get(id=instance.user.id).earnings, (
		"clicks", "conversions", "clicks_today", "conversions_today", "today",
		"week", "month", "year", "total"))

	# Send response to Control Panel
	response = {
		"success": True,
		"message": "Conversion",
		"type": "CONVERSION",
		"data": {
			"conversion": conversion_data,
			"user": user_data
		}
	}

	cp = RedisPublisher(facility="cp", users=[instance.user.username])
	cp.publish_message(RedisMessage(json.dumps(response)), expire=0)