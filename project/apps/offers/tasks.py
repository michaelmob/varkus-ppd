from __future__ import absolute_import
from celery import shared_task
from .utils.sync import sync as _sync
from .models import Earnings


@shared_task
def sync(): 		return _sync()


@shared_task
def reset_today(): 	return Earnings().reset_today()


@shared_task
def reset_week(): 	return Earnings().reset_week()


@shared_task
def reset_month(): 	return Earnings().reset_month()


@shared_task
def reset_year(): 	return Earnings().reset_year()
