from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {

	# Offer Sync
	"offer-sync": {
		"task": "offers.tasks.sync",
		"schedule": crontab(minute="*/15")
	},

	# Invoice Creation
	"create-invoices": {
		"task": "billing.tasks.create_all_invoices",
		"schedule": crontab(minute=0, hour=0, day_of_month="1")
	},

	# Database Backup
	"backup-database": {
		"task": "core.tasks.backup_database",
		"schedule": crontab(minute=0, hour=0)	
	},

	"backup-media": {
		"task": "core.tasks.backup_media",
		"schedule": crontab(minute=0, hour=0)	
	},

	###
	# Keep all resets on bottom!
	###

	# User Resets
	"user-reset-today": {
		"task": "users.tasks.reset_today", 
		"schedule": crontab(minute=0, hour=0)	
	},

	"user-reset-week": {
		"task": "users.tasks.reset_week",
		"schedule": crontab(minute=0, hour=0, day_of_week="sunday")
	},

	"user-reset-month": {
		"task": "users.tasks.reset_month",
		"schedule": crontab(minute=0, hour=0, day_of_month="1")
	},

	"user-reset-year": {
		"task": "users.tasks.reset_year",
		"schedule": crontab(minute=0, hour=0, day_of_month="1", month_of_year="1")
	},

	# Offer Resets
	"offer-reset-today": {
		"task": "offers.tasks.reset_today",
		"schedule": crontab(minute=0, hour=0)
	},
	"offer-reset-week": {
		"task": "offers.tasks.reset_week",
		"schedule": crontab(minute=0, hour=0, day_of_week="sunday")
	},
	"offer-reset-month": {
		"task": "offers.tasks.reset_month",
		"schedule": crontab(minute=0, hour=0, day_of_month="1")
	},
	"offer-reset-year": {
		"task": "offers.tasks.reset_year",
		"schedule": crontab(minute=0, hour=0, day_of_month="1", month_of_year="1")
	},

	# Lockers Resets
	"locker-reset-today": {
		"task": "lockers.tasks.reset_today",
		"schedule": crontab(minute=0, hour=0)
	},
	"locker-reset-week": {
		"task": "lockers.tasks.reset_week",
		"schedule": crontab(minute=0, hour=0, day_of_week="sunday")
	},
	"locker-reset-month": {
		"task": "lockers.tasks.reset_month",
		"schedule": crontab(minute=0, hour=0, day_of_month="1")
	},
	"locker-reset-year": {
		"task": "lockers.tasks.reset_year",
		"schedule": crontab(minute=0, hour=0, day_of_month="1", month_of_year="1")
	}

}
