from django.conf import settings


def get(ip_address):
	return settings.GEOIP.city(ip_address)


def country(ip_address):
	try:
		return get(ip_address).country.iso_code
	except:
		return "US"


def country_region(ip_address):
	obj = get(ip_address)

	return (
		obj.country.iso_code,
		obj.city.name
	)
	