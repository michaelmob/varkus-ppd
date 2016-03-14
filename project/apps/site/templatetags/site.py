from django import template
from django.conf import settings
from utils.strings import random as _random

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
	""" Adds additional context variables to the default context. """
	host = settings.WEBSOCKET_HOST or "ws%s://%s" % (
		("s" if context["request"].is_secure() else ""),
		context["request"].get_host())
	return host + settings.WEBSOCKET_URL

@register.filter
def random(text, length):
	return text + _random(length)

@register.filter
def class_name(klass):
	return klass.__class__.__name__