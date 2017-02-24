from __future__ import absolute_import
from celery import shared_task
from .utils.sync import adgate_sync
from .models import Earnings


@shared_task
def sync():
	"""
	Automatically synchronize offers.
	"""
	return adgate_sync()


@shared_task
def reset_today():
	"""
	Reset today's earnings for Offer.
	"""
	Earnings.run_reset("today")
	return "Reset Offer Earnings: Today"


@shared_task
def reset_week():
	"""
	Reset this week's earnings for Offer.
	"""
	Earnings.run_reset("week")
	return "Reset Offer Earnings: Week"


@shared_task
def reset_month():
	"""
	Reset this month's earnings for Offer.
	"""
	Earnings.run_reset("month")
	return "Reset Offer Earnings: Month"


@shared_task
def reset_year():
	"""
	Reset this year's earnings for Offer.
	"""
	Earnings.run_reset("year")
	return "Reset Offer Earnings: Year"