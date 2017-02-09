from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
geoip = GeoIP2()


def get(ip_address):
	"""
	Return (country code, city) from IP address.
	"""
	if settings.DEBUG:
		return ("US", "Paramus")

	try:
		result = geoip.city(ip_address)
		return (result["country_code"].upper(), result["city"])
	except:
		return (None, None)


def country_code(ip_address):
	"""
	Return country code from IP address.
	"""
	try:
		return geoip.country_code(ip_address).upper()
	except:
		return None