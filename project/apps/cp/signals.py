from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import cache
from apps.conversions.models import Conversion
from apps.lockers.fields import locker_ref_to_object

@receiver(post_save, sender=Conversion)
def charts_conversion_signal(sender, instance, created, **kwargs):
	""" Signal for when a conversion is created, this signal clears cache for
	the charts """
	# Conversion must be being created and token must exist with a user
	if not (created and instance.offer and instance.user and not instance.blocked):
		return

	# Sometimes instance.locker is the reference, and sometimes it's the object
	if isinstance(instance.locker, str):
		instance.locker = locker_ref_to_object(instance.locker)

		if not instance.locker:
			return

	locker_ref = instance.locker.get_type() + str(instance.locker.id)
	user_ref = instance.user.__class__.__name__.lower() + str(instance.user.id)

	# cache.delete_many with memcached doesn't work
	cache_keys = (
		# User's Charts
		"lc_" + user_ref,
		"mc_" + user_ref,

		# User's Locker Charts
		"lc_" + locker_ref,
		"mc_" + locker_ref)

	cache.delete_many(cache_keys)