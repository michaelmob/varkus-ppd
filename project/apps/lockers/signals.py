from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from apps.conversions.models import Conversion
from apps.lockers.fields import locker_ref_to_object

@receiver(post_save, sender=Conversion)
def locker_conversion_signal(sender, instance, created, **kwargs):
	""" Signal for when a conversion is created, this signal adds earnings
		to the locker """
	# Conversion must be being created and user & their profile must exist
	if not (created and instance.locker and not instance.blocked):
		return

	# Sometimes instance.locker is the reference, and sometimes it's the object
	if isinstance(instance.locker, str):
		instance.locker = locker_ref_to_object(instance.locker)

		if not instance.locker:
			return

	# Get user's cut amount
	cut_amount, ref_cut_amount = instance.user.profile.party_cut_amounts()

	# Add to locker's earnings
	instance.locker.earnings.add(instance.payout, cut_amount)


@receiver(post_delete, sender=Conversion)
def locker_conversion_delete_signal(sender, instance, **kwargs):
	""" Signal for when a conversion is deleted, this signal removes earnings
		from the locker """
	# Verify user exists
	if not (instance.locker):
		return

	# Subtract from locker's earnings
	instance.locker.earnings.subtract(instance.user_payout)