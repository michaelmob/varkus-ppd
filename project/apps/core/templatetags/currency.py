from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def currency(value):
	"""
	Return value in a currency format.
	"""
	try:
		value = Decimal(value)
	except:
		value = 0

	return "%.2f" % value


@register.filter
def percentage(value):
	"""
	Return value in a percent format.
	"""
	try:
		value = Decimal(value)
	except:
		value = 0

	return "%.3g%%" % value


@register.filter
def cut_percent(value, percent):
	"""
	Cut percent from number; useful for getting a user's cut amount.
	"""
	if percent == 1:
		return value

	amount_cut = value - (value * percent)
	return currency(amount_cut)
