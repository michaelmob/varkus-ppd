from django import template

from ..models import Notification
from apps.support.models import Contact_Message, Abuse_Report
from apps.tickets.models import Thread
from apps.billing.models import Invoice

register = template.Library()


@register.simple_tag(takes_context=True)
def notifications(context):
	return Notification.get(context["request"].user).order_by("-datetime")[:5]

@register.filter
def has_unread(data):
	for x in data:
		if x.unread == True:
			return True
	return False

@register.simple_tag
def staff_notifications():
	return {
		"messages": Contact_Message.objects.filter(unread=True).count(),
		"reports": Abuse_Report.objects.filter(unread=True).count(),
		"invoices": Invoice.objects.filter(paid=False, error=False).count(),
		"tickets": Thread.objects.filter(closed=False, unread=True).count()
	}