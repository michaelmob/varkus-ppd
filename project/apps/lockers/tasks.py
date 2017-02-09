from celery import shared_task
from django.conf import settings

LOCKERS = [x[0].lower()[:6] for x in settings.LOCKERS]
for name in LOCKERS:
	if name.isalpha():
		exec("from modules.%ss.models import %s" % (name, name.title()))


def run_locker_resets(time_period):
	"""
	Reset all lockers earnings for time_period.
	"""
	for name in LOCKERS:
		if not name.isalpha():
			continue
		
		model = eval(name)
		model.get_earnings_model().run_reset(time_period)

	return "Reset Locker Earnings: %s" % time_period.title()


@shared_task
def reset_today():
	"""
	Reset daily earnings field for all lockers.
	"""
	return run_locker_resets("today")


@shared_task
def reset_week():
	"""
	Reset weekly earnings field for all lockers.
	"""
	return run_locker_resets("week")


@shared_task
def reset_month():
	"""
	Reset monthly earnings field for all lockers.
	"""
	return run_locker_resets("month")


@shared_task
def reset_year():
	"""
	Reset yearly earnings field for all lockers.
	"""
	return run_locker_resets("year")
