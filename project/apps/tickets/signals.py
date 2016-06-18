from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Post
from apps.cp.models import Notification

@receiver(post_save, sender=Post)
def post_create_signal(sender, instance, created, **kwargs):
	""" Signal for when a ticket post is created """
	if not (created and instance.user):
		return

	# Send Notification to User if staff user posted
	if instance.user.is_staff:
		Notification.create(instance.thread.user, "ticket",
			"%s has replied to your ticket." % instance.user.first_name,
			instance.thread.get_absolute_url())

	# Set thread to unread if user is not staff
	instance.thread.unread = not instance.user.is_staff
	instance.thread.save()