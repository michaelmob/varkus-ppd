from datetime import datetime
from hashlib import md5
from django.db import models
from django.contrib.auth.models import User
from ..models import Locker_Base, Earnings_Base


class File(Locker_Base):
	file 		= models.FileField(upload_to="files/%Y/%m/", default=None, blank=True, null=True)
	file_name 	= models.CharField(default="", max_length=300, blank=True, null=True)
	file_size 	= models.IntegerField()
	md5 		= models.CharField(max_length=32, blank=True, null=True)

	def create(user, file):
		obj = File.objects.create(
			user 		= user,
			code 		= File().generate_code(),
			name 		= file.name,
			file 		= file.file,
			file_name	= file.name,
			file_size	= file.size,
			date_time	= datetime.now()
		)

		Earnings.objects.get_or_create(obj=obj)

		return obj


class Earnings(Earnings_Base):
	obj = models.OneToOneField(File, primary_key=True)

	class Meta:
		db_table = "files_earnings"
