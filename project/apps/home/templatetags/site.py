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


@register.simple_tag(takes_context=True)
def websocket_uri(context):
	"""
	Adds additional context variables to the default context.
	"""
	request = context["request"]
	protocol = request.is_secure() and "wss://" or "ws://"
	host = settings.WEBSOCKET_HOST or request.get_host()

	return protocol + host + settings.WEBSOCKET_URL