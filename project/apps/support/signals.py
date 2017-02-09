from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import AbuseReport


@receiver(post_delete, sender=AbuseReport)
def abuse_report_delete_signal(sender, instance, **kwargs):
	"""
	Signal activated when an Abuse Report is deleted.
	This signal deletes leftover files.
	"""
	instance.file1.delete()
	instance.file2.delete()
	instance.file3.delete()