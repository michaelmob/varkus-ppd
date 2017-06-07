from django import template
from django.conf import settings

register = template.Library()


@register.filter
def locker_icon(value):
	"""
	Return icon class associated with locker.
	"""
	return settings.LOCKER_ICONS.get(value.upper(), "lock")