from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import File


@receiver(post_delete, sender=File)
def file_delete_signal(sender, instance, **kwargs):
	"""
	Delete file so they are not orphans.
	"""
	instance.file.delete()