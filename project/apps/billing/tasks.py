from __future__ import absolute_import
from celery import shared_task
from .models import Invoice

@shared_task
def generate():
	return Invoice.generate()