from __future__ import absolute_import
import os
from celery import Celery
from .settings import INSTALLED_APPS
from .beat import CELERYBEAT_SCHEDULE

# set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siren.settings")

app = Celery("siren")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.conf.update(
	CELERY_TIMEZONE="America/New_York",
	CELERY_RESULT_BACKEND="djcelery.backends.database.DatabaseBackend",
	CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler",
	CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE,
)

app.autodiscover_tasks(lambda: INSTALLED_APPS)
