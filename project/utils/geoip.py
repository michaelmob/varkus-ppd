from django.contrib.gis.geoip2 import GeoIP2
geoip = GeoIP2()

def retrieve(ip_address):
	x = geoip.city(ip_address)
	
	try:
		return (x["country_code"], x["city"])
	except:
		return (None, None)