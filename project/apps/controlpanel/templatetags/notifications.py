from django import template
from ..models import Broadcast, Notification

register = template.Library()


@register.simple_tag(takes_context=True)
def notifications_unread(context):
	"""
	Return notification unread count.
	"""
	user = context["request"].user
	count = Broadcast.get_unread_broadcasts(user).count()
	count += Notification.get_unread_notifications(user).count()
	return count