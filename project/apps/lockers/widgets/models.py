from django.conf import settings
from datetime import datetime
from django.db import models
from ..models import Locker_Base, Earnings_Base
from apps.lockers.fields import LockerField


D = { "max_length": 300, "blank": True, "null": True }

class Widget(Locker_Base):
	locker = LockerField()

	custom_css_url 			= models.CharField(default=None, **D)
	http_notification_url 	= models.CharField(default=None, **D)
	standalone_redirect_url = models.CharField(default=settings.SITE_URL, **D)

	def set_locker(self, obj):
		self.locker = obj or None
		self.save()

	def create(user, name, description):
		obj = Widget.objects.create(
			user 			= user,
			code 			= Widget().generate_code(),
			name 			= name,
			description		= description)

		Earnings.objects.get_or_create(obj=obj)

		return obj


class Earnings(Earnings_Base):
	obj = models.OneToOneField(Widget, primary_key=True)

	class Meta:
		db_table = "widgets_earnings"