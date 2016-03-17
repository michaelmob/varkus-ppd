from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.conversions.models import Conversion

@receiver(post_save, sender=Conversion)
def offer_conversion_signal(sender, instance, created, **kwargs):
	""" Signal for when a conversion is created, this signal adds earnings
		to the offer """
	# Conversion must be being created and user & their profile must exist
	if not (created and instance.offer and instance.user and not instance.blocked):
		return

	# Get user's cut amount
	cut_amount, ref_cut_amount = instance.user.profile.party_cut_amounts()

	# Add to offer's earnings
	instance.offer.earnings.add(instance.payout, cut_amount)


@receiver(post_delete, sender=Conversion)
def offer_conversion_delete_signal(sender, instance, **kwargs):
	""" Signal for when a conversion is deleted, this signal removes earnings
		from the offer """
	# Verify offer exists
	if not (instance.offer):
		return

	# Subtract from offer's earnings
	instance.offer.earnings.subtract(instance.user_payout)