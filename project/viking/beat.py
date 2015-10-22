from __future__ import absolute_import
from celery.schedules import crontab
from celery import shared_task

mins 	= crontab(minute="*/1")
quarter = crontab(minute="*/15")
half 	= crontab(minute="*/30")
day 	= crontab(minute=0, hour=0)
week 	= crontab(minute=0, hour=0, day_of_week="sunday")
month 	= crontab(minute=0, hour=0, day_of_month="1")
year 	= crontab(minute=0, hour=0, day_of_month="1", month_of_year="1")

CELERYBEAT_SCHEDULE = {
	# Offer Sync
	"offer-sync"		: {	"task": "apps.offers.tasks.sync", 			"schedule": quarter	},

	# Invoice Creation
	"user-reset-month"	: {	"task": "apps.billing.tasks.generate", 		"schedule": month	},

	###
	# Keep all resets on bottom!
	###

	# User Resets
	"user-reset-today"	: {	"task": "apps.user.tasks.reset_today", 		"schedule": day		},
	"user-reset-week"	: {	"task": "apps.user.tasks.reset_week", 		"schedule": week	},
	"user-reset-month"	: {	"task": "apps.user.tasks.reset_month", 		"schedule": month	},
	"user-reset-year"	: {	"task": "apps.user.tasks.reset_year", 		"schedule": year	},

	# Offer Resets
	"offer-reset-today"	: {	"task": "apps.offers.tasks.reset_today", 	"schedule": day 	},
	"offer-reset-week"	: {	"task": "apps.offers.tasks.reset_week", 	"schedule": week 	},
	"offer-reset-month"	: {	"task": "apps.offers.tasks.reset_month", 	"schedule": month 	},
	"offer-reset-year"	: {	"task": "apps.offers.tasks.reset_year", 	"schedule": year 	},

	# Lockers Resets
	"locker-reset-today": {	"task": "apps.lockers.tasks.reset_today", 	"schedule": day 	},
	"locker-reset-week"	: {	"task": "apps.lockers.tasks.reset_week", 	"schedule": week 	},
	"locker-reset-month": {	"task": "apps.lockers.tasks.reset_month", 	"schedule": month 	},
	"locker-reset-year"	: {	"task": "apps.lockers.tasks.reset_year", 	"schedule": year 	},
}
