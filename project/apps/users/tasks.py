from celery import shared_task
from .models import Earnings, ReferralEarnings


@shared_task
def reset_today():
	"""
	Reset daily earnings field for all rows.
	"""
	# Resets
	Earnings.run_reset("today")
	ReferralEarnings.run_reset("today")
	return "Reset User Earnings: Today"


@shared_task
def reset_week():
	"""
	Reset weekly earnings field for all rows.
	"""
	Earnings.run_reset("week")
	ReferralEarnings.run_reset("week")
	return "Reset User Earnings: Week"


@shared_task
def reset_month():
	"""
	Reset monthly earnings field for all rows.
	"""
	Earnings.run_reset("month")
	ReferralEarnings.run_reset("month")
	return "Reset User Earnings: Month"


@shared_task
def reset_year():
	"""
	Reset yearly earnings field for all rows.
	"""
	Earnings.run_reset("year")
	ReferralEarnings.rese("year")
	return "Reset User Earnings: Year"
