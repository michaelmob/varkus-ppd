import json
from channels import Group

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Conversion, Token


@receiver(post_save, sender=Token)
def unlock_signal(sender, instance, created, **kwargs):
	""" Signal for after a token is saved, this signal is responsible
		for publishing details of the locker to the redis queue but only if
		the token is marked as accessible (meaning the user has access to the
		locker that is attached) """
	if not (instance.locker and instance.session and instance.access()):
		return

	# Send response to Locker
	response = {
		"success": True,
		"message": "Unlocked " + instance.locker.get_type().title(),
		"type": "UNLOCK",
		"data": {
			"locker": instance.locker.get_type(),
			"code": instance.locker.code,
			"url": instance.locker.get_unlock_url()
		}
	}

	Group("session-" + instance.session).send({
		"text": json.dumps(response)
	})


@receiver(post_save, sender=Token)
def notify_click_signal(sender, instance, created, **kwargs):
	""" Signal for when a token is created, this signal is responsible
		for publishing details of the token to the redis queue that will,
		in turn, notify the user a click has went through """
	if not (created and instance.user):
		return

	response = {
		"success": True,
		"type": "TOKEN"
	}

	Group("user-" + str(instance.user.pk)).send({
		"text": json.dumps(response)
	})


@receiver(post_save, sender=Conversion)
def notify_conversion_signal(sender, instance, created, **kwargs):
	""" Signal for when a conversion is created, this signal is responsible
		for publishing details of the conversion to the redis queue that will,
		in turn, notify the user a conversion has went through """
	if not (created and instance.user and not instance.blocked):
		return

	# Keep wanted user data
	earnings = User.objects.get(id=instance.user.id).earnings

	# Send response to Control Panel
	response = {
		"success": True,
		"type": "CONVERSION",
		"data": {
			"approved": True,
			"payout": float(instance.user_payout),
			"user": earnings.output_dict()
		}
	}

	Group("user-" + str(instance.user.pk)).send({
		"text": json.dumps(response)
	})