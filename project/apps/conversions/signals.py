import json
from channels import Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Conversion, Token


@receiver(pre_save, sender=Conversion)
def conversion_signal(sender, instance, **kwargs):
	"""
	Pre-save signal to update all conversion fields.
	"""
	if not instance._state.adding or instance.is_blocked:
		instance.do_not_add = True
		return

	# User and profile must exist
	user = instance.user
	if not (user and user.profile):
		instance.do_not_add = True
		return

	# Get cut amounts and calculate payouts
	cut_amount, referral_cut_amount = user.profile.get_cut_amounts()
	payout = instance.payout - (instance.payout * cut_amount)

	# Set instance fields
	instance.dev_payout = instance.payout - payout
	instance.payout = payout

	# Referral
	if user.profile and user.profile.referrer and user.referralearnings:
		instance.referral_payout = payout * referral_cut_amount


@receiver(post_save, sender=Conversion)
def notify_conversion_signal(sender, instance, created, **kwargs):
	"""
	Signal for when a conversion is created, this signal is responsible
	for publishing details of the conversion to the redis queue that will,
	in turn, notify the user a conversion has went through
	"""
	if not (created and instance.user and not instance.is_blocked):
		return

	# Keep wanted user data
	earnings = User.objects.get(id=instance.user.id).earnings

	# Send response to Control Panel
	response = {
		"success": True,
		"type": "CONVERSION",
		"data": {
			"approved": True,
			"payout": float(instance.payout),
			"user": earnings.output_dict()
		}
	}

	Group("user-" + str(instance.user.pk)).send({
		"text": json.dumps(response)
	})


@receiver(post_save, sender=Token)
def unlock_signal(sender, instance, created, **kwargs):
	"""
	Signal for after a token is saved, this signal is responsible
	for publishing details of the locker to the redis queue but only if
	the token is marked as accessible (meaning the user has access to the
	locker that is attached)
	"""
	if not (instance.locker and instance.session and instance.has_access):
		return

	# Send response to Locker
	response = {
		"success": True,
		"message": "Unlocked " + instance.locker.type.title(),
		"type": "UNLOCK",
		"data": {
			"locker": instance.locker.type,
			"code": instance.locker.code,
			"url": instance.locker.get_unlock_url()
		}
	}

	Group("session-" + instance.session).send({
		"text": json.dumps(response)
	})


@receiver(post_save, sender=Token)
def notify_click_signal(sender, instance, created, **kwargs):
	"""
	Signal for when a token is created, this signal is responsible
	for publishing details of the token to the redis queue that will,
	in turn, notify the user a click has went through
	"""
	if not (created and instance.user):
		return

	response = {
		"success": True,
		"type": "TOKEN"
	}

	Group("user-" + str(instance.user.pk)).send({
		"text": json.dumps(response)
	})