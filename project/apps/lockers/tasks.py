from __future__ import absolute_import
from celery import shared_task

from .widgets.models import Widget_Earnings
from .files.models import File_Earnings
from .link.models import Link_Earnings
from .list.models import List_Earnings

#@shared_task
#def increment_click(obj, ip_address):
#	return obj.earnings.increment_clicks(ip_address)

@shared_task
def reset_today():
	return Widget_Earnings().reset_today()
	return File_Earnings().reset_today()
	return Link_Earnings().reset_today()
	return List_Earnings().reset_today()

@shared_task
def reset_week():
	return Widget_Earnings().reset_week()
	return File_Earnings().reset_week()
	return Link_Earnings().reset_week()
	return List_Earnings().reset_week()

@shared_task
def reset_month():
	return Widget_Earnings().reset_month()
	return File_Earnings().reset_month()
	return Link_Earnings().reset_month()
	return List_Earnings().reset_month()

@shared_task
def reset_year():
	return Widget_Earnings().reset_year()
	return File_Earnings().reset_year()
	return Link_Earnings().reset_year()
	return List_Earnings().reset_year()
