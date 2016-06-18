from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ..models import Locker_Base, Earnings_Base
from utils.constants import BLANK_NULL

DEFAULTS = { "max_length": 300, "blank": True, "null": True }


class Widget(Locker_Base):
	locker_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, limit_choices_to={"app_label__in": ("lockers",)}, **BLANK_NULL)
	locker_id 	= models.PositiveIntegerField(**BLANK_NULL)
	locker 		= GenericForeignKey("locker_type", "locker_id")

	custom_css_url 			= models.CharField(default=None, **DEFAULTS)
	http_notification_url 	= models.CharField(default=None, **DEFAULTS)
	standalone_redirect_url = models.CharField(default=settings.SITE_URL, **DEFAULTS)

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