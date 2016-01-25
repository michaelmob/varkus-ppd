from __future__ import absolute_import
from celery import shared_task

from .widgets.models import Earnings as Widget_Earnings
from .files.models import Earnings as File_Earnings
from .links.models import Earnings as Link_Earnings
from .lists.models import Earnings as List_Earnings

@shared_task
def reset_today():
	return (
		Widget_Earnings().reset_today(),
		File_Earnings().reset_today(),
		Link_Earnings().reset_today(),
		List_Earnings().reset_today()
	)

@shared_task
def reset_week():
	return (
		Widget_Earnings().reset_week(),
		File_Earnings().reset_week(),
		Link_Earnings().reset_week(),
		List_Earnings().reset_week()
	)

@shared_task
def reset_month():
	return (
		Widget_Earnings().reset_month(),
		File_Earnings().reset_month(),
		Link_Earnings().reset_month(),
		List_Earnings().reset_month()
	)

@shared_task
def reset_year():
	return (
		Widget_Earnings().reset_year(),
		File_Earnings().reset_year(),
		Link_Earnings().reset_year(),
		List_Earnings().reset_year()
	)
