from __future__ import absolute_import
from celery import shared_task


@shared_task
def increment_click(obj, ip_address):
	return obj.earnings.increment_clicks(ip_address)

#from ...tasks import increment_click
#increment_click.delay(obj, request.META["REMOTE_ADDR"])
