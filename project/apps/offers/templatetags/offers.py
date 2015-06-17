from django import template
from django.conf import settings

register = template.Library()


@register.filter
def category_icon(category):
	try:
		return "<i class=\"%s icon\"></i>" % settings.CATEGORY_TYPES_ICONS[category]
	except:
		return ""
