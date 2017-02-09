from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from conversions.models import Conversion


@receiver(post_save, sender=Conversion)
def offer_conversion_signal(sender, instance, created, **kwargs):
	"""
	Signal is activated when a conversion is created. This signal adds earnings
	to the offer.
	"""
	if created and instance.offer and instance.user:
		instance.offer.earnings.add(instance, "total_payout")


@receiver(post_delete, sender=Conversion)
def offer_conversion_delete_signal(sender, instance, **kwargs):
	"""
	Signal is activated when a conversion is deleted. This signal removes
	earnings from the offer.
	"""
	if instance.offer:
		instance.offer.earnings.remove(instance, "total_payout")