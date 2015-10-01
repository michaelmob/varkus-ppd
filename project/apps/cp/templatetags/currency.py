from django import template
from decimal import Decimal, getcontext

register = template.Library()


@register.filter
def currency(value):
	try:
		value = Decimal(value)
	except:
		value = 0

	return "%.2f" % value


@register.filter
def cut_percent(value, percent):
	getcontext().prec = 2
	value = Decimal(value)
	amount_cut = (value - (value * Decimal(percent)))

	return currency(amount_cut)

