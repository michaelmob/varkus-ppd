from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from billing.models import Billing
from conversions.models import Conversion
from .models import Profile, Party, Earnings, ReferralEarnings


@receiver(post_save, sender=User)
def user_saved_signal(sender, instance, created, **kwargs):
	"""
	Signal activated after user is saved.
	"""
	if not created:
		return

	Profile.objects.get_or_create(user=instance, defaults={
		"party": Party.get_or_create_default()
	})
	Billing.objects.get_or_create(user=instance)
	Earnings.objects.get_or_create(parent=instance)
	ReferralEarnings.objects.get_or_create(parent=instance)


@receiver(post_save, sender=Conversion)
def user_conversion_signal(sender, instance, created, **kwargs):
	"""
	Signal activated when user receives a conversion.
	"""
	if not (created and instance.user):
		return
	
	instance.user.earnings.add(instance)

	# Remove from referrer
	referrer = instance.user.profile.referrer
	if referrer and referrer.referralearnings:
		referrer.referralearnings.add(instance, "referral_payout")


@receiver(post_delete, sender=Conversion)
def user_conversion_delete_signal(sender, instance, **kwargs):
	"""
	Signal for when a conversion is deleted.
	This signal removes earnings from the user's earnings.
	"""
	# Verify user exists
	user = instance.user
	if not (user and user.earnings and user.profile):
		return

	# Remove earnings from user
	user.earnings.remove(instance)

	# Remove from referrer
	referrer = user.profile.referrer
	if referrer and referrer.referralearnings:
		referrer.referralearnings.remove(instance, "referral_payout")