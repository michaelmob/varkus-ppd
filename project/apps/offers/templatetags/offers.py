from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def redirect_url(offer, obj):
	return offer.get_redirect_url(obj)


@register.filter
def render_icon(icon):
	return mark_safe("<div class=\"icon\"><i class=\"%s icon\"></i></div>" % icon)


@register.filter
def render_cat_icon(category):
	icon = settings.CATEGORY_TYPES_ICONS.get(category)

	if not icon:
		return ""

	return render_icon(icon)