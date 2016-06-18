from datetime import date, timedelta
from calendar import monthrange

from django import template
from django.conf import settings
from ..models import PAYMENT_ICONS

register = template.Library()


@register.filter
def payment_icon(method):
	try:
		return "<i class=\"%s icon\"></i>" % PAYMENT_ICONS[method]
	except:
		return "<i class=\"payment icon\"></i>"


@register.filter
def payment_next_date(freq):
	today = date.today()
	
	return date(today.year, today.month,
		monthrange(today.year, today.month)[1]) + timedelta(days=int(freq))