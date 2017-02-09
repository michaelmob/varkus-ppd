from django import template
from django.contrib.auth.models import User
from billing.models import Invoice
from tickets.models import Thread


register = template.Library()


@register.simple_tag
def users_unapproved():
	"""
	Return count of unapproved users.
	"""
	return User.objects.filter(is_active=False).count()


@register.simple_tag
def invoices_unpaid():
	"""
	Return count of unpaid invoices that are not marked as an error.
	"""
	return Invoice.objects.filter(paid=False, error=False).count()


@register.simple_tag
def tickets_unread():
	"""
	Return count of tickets that need to be responded to.
	"""
	return Thread.objects.filter(staff_unread=True, closed=False).count()