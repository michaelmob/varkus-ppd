from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag()
def site_name():
	return settings.SITE_NAME


@register.simple_tag()
def site_url():
	return settings.SITE_URL


@register.simple_tag()
def site_domain():
	return settings.SITE_DOMAIN