from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from conversions.models import Conversion


@receiver(post_save, sender=Conversion)
def locker_conversion_signal(sender, instance, created, **kwargs):
	"""
	Signal for when a conversion is created.
	This signal adds earnings to the locker object.
	"""
	if created and instance.locker:
		instance.locker.earnings.add(instance)


@receiver(post_delete, sender=Conversion)
def locker_conversion_delete_signal(sender, instance, **kwargs):
	"""
	Signal for when a conversion is deleted.
	This signal removes earnings from the locker object.
	"""
	if instance.locker:
		instance.locker.earnings.remove(instance)