from django import template
from urllib.parse import quote

register = template.Library()


@register.simple_tag
def facebook(url):
	"""
	Returns Facebook share URL.
	"""
	return "https://facebook.com/sharer/sharer.php?u=" + url


@register.simple_tag()
def googleplus(url):
	"""
	Returns Google+ share URL.
	"""
	return "https://plus.google.com/share?url=" + url


@register.simple_tag
def twitter(url, message):
	"""
	Returns Twitter share URL with message.
	"""
	return "https://twitter.com/intent/tweet?url=%s&text=%s" % (
		url, quote(message),
	)


@register.simple_tag
def email(subject, message):
	"""
	Returns E-mail mailto URL.
	"""
	return "mailto:?subject=%s&body=%s" % (
		quote(subject), quote(message)
	)