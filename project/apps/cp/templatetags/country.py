from django import template
from utils.country import COUNTRIES

register = template.Library()

@register.filter
def country(code):
	if code == "intl":
		return "International"

	try:
		return COUNTRIES[str(code).upper()]
	except:
		return "Unknown"