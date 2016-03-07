from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.api.views.notifications import notify
from apps.conversions.models import Conversion
from apps.lockers.fields import locker_ref_to_object


@receiver(post_save, sender=Conversion)
def send_widget_http_notification(sender, **kwargs):
	if not kwargs["created"]:
		return

	conversion = Conversion.objects.get(pk=kwargs["instance"].pk)

	# Send HTTP Notification only if Widget
	if conversion.locker.get_type() != "widget":
		return

	# Stop conversion_blocked notification
	if conversion.conversion_blocked:
		return

	url = conversion.locker.http_notification_url

	if url and len(url) > 20:
		notify(conversion)