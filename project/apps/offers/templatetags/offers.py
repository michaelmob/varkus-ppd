from django import template
from django.utils.safestring import mark_safe
from ..constants import CATEGORY_TYPES_ICONS
from ..utils.offers import mock_offer

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
	try:
		return offer.get_redirect_url(object_)
	except AttributeError:
		return "#"


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
	icon = CATEGORY_TYPES_ICONS.get(category)

	if not icon:
		icon = "tag"

	return render_icon(icon)


@register.simple_tag
def mock_offers():
	"""
	Returns list of mock offers.
	"""
	return [
		mock_offer("Downloads", "Offer 1", priority=True),
		mock_offer("Free", "Offer 2"),
		mock_offer("iPad", "Offer 3"),
		mock_offer("iPhone", "Offer 4"),
		mock_offer("Conversion Gen", "Offer 5")
	]