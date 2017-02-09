from django.db.models.signals import post_save
from django.dispatch import receiver
from conversions.models import Conversion
from .views.webhooks import send_payload


@receiver(post_save, sender=Conversion)
def send_widget_notification(sender, instance, created, **kwargs):
	""" 
	Signal for when a conversion is created, this signal sends a callback to the
	widget's webhook url.
	"""
	if not (created and instance.locker) or instance.is_blocked:
		return

	# Widgets only!
	if instance.locker.type != "widget":
		return

	send_payload(instance)