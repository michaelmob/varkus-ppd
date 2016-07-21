from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def site_name():
	return settings.SITE_NAME

@register.simple_tag
def site_domain():
	return settings.SITE_DOMAIN

@register.simple_tag(takes_context=True)
def websocket_url(context):
	""" Get websocket url """
	return "%s://%s/ws" % (
		"wss" if context["request"].is_secure() else "ws",
		context["request"].get_host()
	)