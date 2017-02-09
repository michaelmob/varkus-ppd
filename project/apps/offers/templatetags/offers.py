from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def priority(object_, user):
	"""
	Determine whether object_ect is priority or is blocked.
	"""
	if object_ in user.profile.offer_block.all():
		return "block"
	elif object_ in user.profile.offer_priority.all():
		return "priority"
	else:
		return "neutral"


@register.filter
def redirect_url(offer, object_):
	"""
	Returns Offer redirect based on the object.
	"""
	return offer.get_redirect_url(object_)


@register.filter
def render_icon(value):
	"""
	Return icon tag.
	"""
	return mark_safe("<i class=\"%s icon\"></i>" % value)


@register.filter
def render_category_icon(category):
	"""
	Returns category icon or None if the category has no icon.
	"""
	icon = settings.CATEGORY_TYPES_ICONS.get(category)

	if not icon:
		icon = "tag"

	return render_icon(icon)