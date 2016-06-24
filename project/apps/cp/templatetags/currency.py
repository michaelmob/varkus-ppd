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
def percentage(value):
	try:
		value = Decimal(value)
	except:
		value = 0

	return "%.3g%%" % value


@register.filter
def cut_percent(value, percent):
	"""Cut percent from number; useful for getting a user's cut amount
	
	Args:
	    value (DECIMAL): Original value
	    percent (INTEGER): Percent to be cut
	
	Returns:
	    STRING: Percentage removed from value
	"""
	amount_cut = value - (value * percent)
	return currency(amount_cut)
