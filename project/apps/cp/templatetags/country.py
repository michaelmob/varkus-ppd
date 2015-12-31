from django import template
from django_countries import countries

register = template.Library()


@register.filter
def country(code):
	if code == "intl":
		return "International"

	try:
		return dict(countries)[str(code).upper()]
	except:
		return "Unknown"