from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from controlpanel.models import Notification
from .models import Post


@receiver(post_save, sender=Post)
def post_create_signal(sender, instance, created, **kwargs):
	"""
	Signal that is activated when a Ticket is posted to.
	"""
	if not (created and instance.user):
		return

	# When the last_user_id has changed there is a new replier
	new_reply = instance.user_id != instance.thread.last_user_id

	# Send Notification to User
	if new_reply and instance.thread.last_user_id:
		Notification.objects.create_notification(
			recipient=instance.user,
			icon="ticket",
			content="Your ticket has a new response.",
			url=instance.get_absolute_url()
		)

	# Set thread's unread status and set the last replier field
	instance.thread.unread = new_reply
	instance.thread.last_user = instance.user
	instance.thread.staff_unread = not instance.user.is_staff
	instance.thread.save()


@receiver(post_delete, sender=Post)
def post_delete_signal(sender, instance, **kwargs):
	"""
	Signal activated when an Abuse Report is deleted.
	This signal removes empty threads and deletes leftover files.
	"""
	instance.file.delete()

	if instance.thread and not instance.thread.get_posts().exists():
		instance.thread.delete()