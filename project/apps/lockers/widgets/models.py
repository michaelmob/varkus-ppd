from django.conf import settings
from datetime import datetime
from django.db import models
from ..models import Locker_Base, Earnings_Base

import apps.lockers.utils

class Widget(Locker_Base):
	locker		= models.CharField(max_length=10, choices=settings.LOCKERS, default=None, blank=True, null=True)
	locker_id	= models.IntegerField(default=None, blank=True, null=True)
	locker_code	= models.CharField(max_length=10, default=None, blank=True, null=True)

	postback_url = models.CharField(max_length=300, default=None, blank=True, null=True)
	custom_css = models.CharField(max_length=300, default=None, blank=True, null=True)
	standalone_redirect = models.CharField(max_length=300, default="https://varkus.com/", blank=True, null=True)

	def __str__(self):
		return "%s: %s" % (self.pk, self.name)


	def set_locker(self, obj):
		if obj == None:
			self.locker 		= None
			self.locker_id 		= None
			self.locker_code 	= None
		else:
			self.locker 		= obj.get_name().upper()
			self.locker_id 		= obj.id
			self.locker_code 	= obj.code
		self.save()


	def locker_object(self):
		try:
			return apps.lockers.utils.Locker(self.locker).objects.get(id=self.locker_id)
		except:
			return None


	def create(user, name, description):
		obj = Widget.objects.create(
			user 			= user,
			code 			= Widget().generate_code(),
			name 			= name,
			description		= description,
			date_time 		= datetime.now(),
		)

		Earnings.objects.get_or_create(obj=obj)

		return obj



class Earnings(Earnings_Base):
	obj 		= models.OneToOneField(Widget, primary_key=True)

	class Meta:
		verbose_name = "Earnings"
		verbose_name_plural = "Earnings"
