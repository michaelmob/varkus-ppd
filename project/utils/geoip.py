from django.contrib.gis.geoip2 import GeoIP2
geoip = GeoIP2()

def retrieve(ip_address):
	x = geoip.city(ip_address)
	
	try:
		return (x["country_code"], x["city"])
	except:
		return (None, None)

def country_code(ip_address):
	try:
		return geoip.country_code(ip_address)
	except:
		return None