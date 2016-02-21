from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.api.views.notifications import notify
from apps.leads.models import Lead
from apps.lockers.fields import locker_ref_to_object


@receiver(post_save, sender=Lead)
def send_widget_http_notification(sender, **kwargs):
	if not kwargs["created"]:
		return

	lead = Lead.objects.get(pk=kwargs["instance"].pk)

	# Send HTTP Notification only if Widget
	if lead.locker.get_type() != "widget":
		return

	# Stop lead_blocked notification
	if lead.lead_blocked:
		return

	url = lead.locker.http_notification_url

	if url and len(url) > 20:
		notify(lead)