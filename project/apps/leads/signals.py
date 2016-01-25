import json
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from .models import Lead, Token


def keep_wanted(obj, wanted):
	result = {}

	for key, val in vars(obj).items():
		if key in wanted:
			if isinstance(val, Decimal):
				val = "%.2f" % val
			result[key] = val

	return result


@receiver(post_save, sender=Token)
def token_created(sender, **kwargs):
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


@receiver(post_save, sender=Lead)
def lead_created(sender, **kwargs):
	if not kwargs["created"]:
		return

	# Lead object
	lead = kwargs["instance"]

	# Add wanted data to lead_data
	lead_data = keep_wanted(lead, (
		"user_payout", "referral_payout", "approved"))

	# Keep wanted user data
	user_data = keep_wanted(User.objects.get(id=lead.user.id).earnings, (
		"clicks", "leads", "clicks_today", "leads_today", "today",
		"week", "month", "year", "total"))

	# Send response to Control Panel
	response = {
		"success": True,
		"message": "Lead",
		"type": "LEAD",
		"data": {
			"lead": lead_data,
			"user": user_data
		}
	}

	cp = RedisPublisher(facility="cp", users=[lead.user.username])
	cp.publish_message(RedisMessage(json.dumps(response)), expire=0)

	# Send response to Locker
	response = {
		"success": True,
		"message": "Unlocked " + lead.locker.get_type().title(),
		"data": {
			"locker": lead.locker.get_type(),
			"code": lead.locker.code,
			"url": lead.locker.get_unlock_url()
		}
	}

	if not lead.token.session:
		return

	locker = RedisPublisher(facility="locker", sessions=[lead.token.session])
	locker.publish_message(RedisMessage(json.dumps(response)))
