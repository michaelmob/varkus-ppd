from __future__ import absolute_import
import os
from celery import Celery
from .settings import INSTALLED_APPS
from .beat import CELERYBEAT_SCHEDULE

# set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "viking.settings")

app = Celery("viking")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.conf.beat_schedule = CELERYBEAT_SCHEDULE
app.conf.update(
    timezone="America/New_York",
	task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
	result_backend="django-db",
	broker_url="amqp://guest:guest@127.0.0.1:5672//"
)

app.autodiscover_tasks(lambda: INSTALLED_APPS)
