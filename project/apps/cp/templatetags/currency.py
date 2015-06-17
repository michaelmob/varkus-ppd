from django import template

register = template.Library()


@register.filter
def currency(value):
	try:
		value = float(value)
	except:
		value = 0

	return "%.2f" % value


@register.filter
def cut_percent(value, percent):
	return currency(value - (value * percent))
