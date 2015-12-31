from django.conf import settings
from datetime import datetime
from django.db import models
from ..models import Locker_Base, Earnings_Base
from apps.lockers.fields import LockerField

class Widget(Locker_Base):
	locker = LockerField()

	postback_url = models.CharField(max_length=300, default=None, blank=True, null=True)
	custom_css_url = models.CharField(max_length=300, default=None, blank=True, null=True)
	standalone_redirect_url = models.CharField(max_length=300, default=settings.SITE_URL, blank=True, null=True)

	def set_locker(self, obj):
		self.locker = obj or None
		self.save()

	def create(user, name, description):
		obj = Widget.objects.create(
			user 			= user,
			code 			= Widget().generate_code(),
			name 			= name,
			description		= description
		)

		Earnings.objects.get_or_create(obj=obj)

		return obj


class Earnings(Earnings_Base):
	obj = models.OneToOneField(Widget, primary_key=True)

	class Meta:
		db_table = "widgets_earnings"