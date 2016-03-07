import json
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from .models import Conversion, Token


def keep_wanted(obj, wanted):
	result = {}

	for key, val in vars(obj).items():
		if key in wanted:
			if isinstance(val, Decimal):
				val = "%.2f" % val
			result[key] = val

	return result


@receiver(post_save, sender=Token)
def send_click_notification(sender, **kwargs):
	if not kwargs["created"]:
		return

	earnings = kwargs["instance"].user.earnings

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

	redis_publisher = RedisPublisher(facility="cp", users=[kwargs["instance"].user.username])
	redis_publisher.publish_message(RedisMessage(json.dumps(response)), expire=0)


@receiver(post_save, sender=Conversion)
def send_conversion_notification(sender, **kwargs):
	if not kwargs["created"]:
		return

	# Conversion object
	conversion = kwargs["instance"]

	# Add wanted data to conversion_data
	conversion_data = keep_wanted(conversion, (
		"user_payout", "referral_payout", "approved"))

	# Keep wanted user data
	user_data = keep_wanted(User.objects.get(id=conversion.user.id).earnings, (
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

	cp = RedisPublisher(facility="cp", users=[conversion.user.username])
	cp.publish_message(RedisMessage(json.dumps(response)), expire=0)

	# Send response to Locker
	response = {
		"success": True,
		"message": "Unlocked " + conversion.locker.get_type().title(),
		"data": {
			"locker": conversion.locker.get_type(),
			"code": conversion.locker.code,
			"url": conversion.locker.get_unlock_url()
		}
	}

	if not conversion.token.session:
		return

	locker = RedisPublisher(facility="locker", sessions=[conversion.token.session])
	locker.publish_message(RedisMessage(json.dumps(response)))