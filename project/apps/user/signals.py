from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import User

from apps.user.models import Profile, Billing, Earnings, Referral_Earnings
from apps.conversions.models import Conversion


@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
	if created:
		Profile.objects.get_or_create(user=instance)
		Billing.objects.get_or_create(user=instance)
		Earnings.objects.get_or_create(obj=instance)
		Referral_Earnings.objects.get_or_create(obj=instance)


@receiver(pre_save, sender=Conversion)
def user_conversion_signal(sender, instance, **kwargs):
	# Conversion must be being created and user & their profile must exist
	if not (instance._state.adding and instance.user and instance.user.profile
		and not instance.blocked):
		return

	# Shortcut
	user = instance.user

	# Get cut_amount
	cut_amount, ref_cut_amount = user.profile.party_cut_amounts()

	# Add to user's earnings
	user_payout = user.earnings.add(instance.payout, cut_amount)

	# Add to referrer's earnings
	referral_payout = 0.00
	if user.profile.referrer and user.profile.referrer.referral_earnings:
		referral_payout = user.profile.referrer.referral_earnings.difference(
			user_payout, ref_cut_amount)

	# Set instance information
	instance.dev_payout			= instance.payout - user_payout
	instance.user_payout		= user_payout
	instance.referral_payout 	= referral_payout


@receiver(post_delete, sender=Conversion)
def user_conversion_delete_signal(sender, instance, **kwargs):
	# Verify user exists
	if not (instance.user and instance.user.profile):
		return

	user = instance.user
	user.earnings.subtract(instance.user_payout)

	if user.profile.referrer and user.profile.referrer.referral_earnings:
		user.profile.referrer.referral_earnings.subtract(instance.referral_payout)