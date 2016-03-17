from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.api.views.notifications import notify
from apps.conversions.models import Conversion
from apps.lockers.fields import locker_ref_to_object


@receiver(post_save, sender=Conversion)
def send_widget_http_notification(sender, instance, created, **kwargs):
	""" Signal for when a conversion is created, this signal sends an HTTP
		notification to the widget's notification url """
	if not (created and instance.locker and not instance.blocked):
		return

	conversion = Conversion.objects.get(pk=instance.pk)

	# Send HTTP Notification only if Widget
	if conversion.locker.get_type() != "widget":
		return

	# Stop blocked notification
	if conversion.blocked:
		return

	url = conversion.locker.http_notification_url

	# Send the notification
	if url and len(url) > 20:
		notify(conversion)