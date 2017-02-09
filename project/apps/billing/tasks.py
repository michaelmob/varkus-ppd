from __future__ import absolute_import
from celery import shared_task
from .models import Invoice


@shared_task
def create_all_invoices():
	"""
	Create all invoices.
	"""
	count = Invoice.objects.create_all_invoices()
	return "Invoices Created: %s" % count