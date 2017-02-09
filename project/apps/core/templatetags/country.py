from django import template
from viking.utils.country import COUNTRIES

register = template.Library()


@register.filter
def country(country_code):
	"""
	Return country name from country code.
	"""
	if country_code == "intl":
		return "International"

	try:
		return COUNTRIES[str(country_code).upper()]
	except:
		return "Unknown"