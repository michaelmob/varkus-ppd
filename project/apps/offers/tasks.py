from __future__ import absolute_import
from celery import shared_task
from .utils.sync import adgate_sync
from .models import Earnings


@shared_task
def sync(): 		return adgate_sync()


@shared_task
def reset_today(): return Earnings().reset_today()


@shared_task
def reset_week(): 	return Earnings().reset_week()


@shared_task
def reset_month(): 	return Earnings().reset_month()


@shared_task
def reset_year(): 	return Earnings().reset_year()
