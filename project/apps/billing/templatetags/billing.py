from datetime import date, timedelta
from calendar import monthrange
from django import template
from django.utils.safestring import mark_safe
from ..constants import PAYMENT_ICONS


register = template.Library()


@register.filter
def payment_icon(method):
	"""
	Return HTML content for an icon.
	"""
	icon = PAYMENT_ICONS.get(method, "payment")
	return "<i class=\"%s icon\"></i>" % icon


@register.filter
def payment_humanize(method):
	"""
	Humanize payment method text.
	"""
	method = method.title()

	if method == "Paypal":
		method = "PayPal"

	return method


@register.filter
def payment_next_date(frequency):
	"""
	Returns next payment date based on payout frequency.
	"""
	today = date.today()
	date = date(today.year, today.month, monthrange(today.year, today.month)[1])
	return date + timedelta(days=int(frequency))