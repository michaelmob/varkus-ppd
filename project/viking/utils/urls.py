from urllib.parse import unquote as _unquote
from django.core.validators import URLValidator


def unquote(url):
	"""
	Wrapper for urllib's unquote function.
	"""
	if url is None:
		return

	return _unquote(url)


def valid(url):
	"""
	Returns True if 'url' is valid.
	"""
	try:
		URLValidator()(url)
		return True
	except:
		return False