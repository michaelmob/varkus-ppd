from celery import shared_task
from django.conf import settings
from django.core.management import call_command


@shared_task
def backup_database():
	"""
	Run database backup command.
	"""
	call_command("dbbackup", "--clean")


@shared_task
def backup_media():
	"""
	Run media backup command.
	"""
	call_command("mediabackup", "--clean")