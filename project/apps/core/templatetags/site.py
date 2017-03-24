from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def site_name():
	"""
	Returns 'SITE_NAME' from settings.
	"""
	return settings.SITE_NAME


@register.simple_tag
def site_domain():
	"""
	Returns 'SITE_DOMAIN' from settings.
	"""
	return settings.SITE_DOMAIN


@register.simple_tag(takes_context=True)
def websocket_url(context):
	"""
	Returns full websocket URL.
	"""
	return "%s://%s/ws" % (
		"wss" if context["request"].is_secure() else "ws",
		context["request"].get_host()
	)


@register.simple_tag(takes_context=True)
def base_url(context):
	"""
	Returns base URL.
	"""
	return context["request"].build_absolute_uri("/")[:-1]