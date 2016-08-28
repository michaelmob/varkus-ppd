import json
from decimal import Decimal
from datetime import datetime, date, timedelta

from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import User

from utils.constants import CURRENCY, BLANK_NULL
import apps.conversions as conversions
from apps.cp.templatetags.currency import currency


NOTIFICATION_ICONS = (
	("announcement", "Announcement"),
	("warning", "Warning"),
	("help", "Help"),
	("info", "Info"),
	("money", "Money"),
	("lightning", "Conversion"),
	("users", "Users"),
	("ticket", "Ticket"),
	("birthday", "Birthday"),
	("alarm", "Alarm"))

NOTIFICATION_COLORS = (
	("blue", "Blue"),
	("red", "Red"),
	("yellow", "Yellow"),
	("orange", "Orange"),
	("green", "Green"))


class Notification(models.Model):
	user		= models.ForeignKey(User, blank=True, null=True)
	icon 		= models.CharField(max_length=15, choices=NOTIFICATION_ICONS)
	color 		= models.CharField(max_length=15, choices=NOTIFICATION_COLORS)
	message 	= models.TextField(max_length=300)
	url 		= models.URLField(max_length=300, **BLANK_NULL)
	unread 		= models.BooleanField(default=True)
	staff 		= models.BooleanField(default=False)
	datetime	= models.DateTimeField(verbose_name="Date")

	def get(user):
		""" Filter notifications from user that are less than 3 days old """
		return __class__.objects.filter(
			Q(user=user, datetime__gt=datetime.now() - timedelta(days=3)) | \
			Q(staff=user.is_staff))

	def create(user, icon, message, url=None, staff=False):
		# Check for older notification and overwrite it
		obj = __class__.objects.filter(user=user, message=message).first()

		# Notification does not exist, so create a new one
		if not obj:
			obj = Notification()
			obj.user = user
			obj.icon = icon
			obj.message = message
			obj.staff = staff

		# Set URL
		if url:
			obj.url = url

		obj.unread = True
		obj.save()

	def mark_read(user):
		return __class__.objects.filter(Q(user=user, unread=True) | \
			Q(staff=user.is_staff)).update(unread=False)

	def clear():
		"""Clear/delete expired notifications"""
		return __class__.objects.filter(
			datetime__lt=datetime.now() - timedelta(days=3), read=True).delete()


class Announcement(models.Model):
	user		= models.ForeignKey(User, blank=True, null=True)
	icon 		= models.CharField(max_length=15, choices=NOTIFICATION_ICONS)
	color 		= models.CharField(max_length=15, choices=NOTIFICATION_COLORS)
	subject 	= models.TextField(max_length=300)
	message 	= models.TextField(max_length=1000)
	broadcast 	= models.BooleanField(default=False)
	datetime	= models.DateTimeField(auto_now_add=True, verbose_name="Date")

	def broadcasts():
		""" Return broadcasts """
		return __class__.objects.filter(broadcast=True)

	def recent():
		return __class__.objects.filter(
			datetime__gt=datetime.now() - timedelta(days=3), read=True).delete()


class Earnings_Base(models.Model):
	clicks			= models.IntegerField(default=0, verbose_name="Clicks")
	conversions		= models.IntegerField(default=0)

	clicks_today	= models.IntegerField(default=0, verbose_name="Today's Clicks")
	conversions_today = models.IntegerField(default=0, verbose_name="Today's Conversions")

	today			= models.DecimalField(verbose_name="Today", **CURRENCY)
	yesterday		= models.DecimalField(verbose_name="Yesterday", **CURRENCY)
	week			= models.DecimalField(verbose_name="Week", **CURRENCY)
	month			= models.DecimalField(verbose_name="Month", **CURRENCY)
	yestermonth		= models.DecimalField(verbose_name="Last Month", **CURRENCY)
	year 			= models.DecimalField(verbose_name="Year", **CURRENCY)
	total			= models.DecimalField(verbose_name="Total", **CURRENCY)

	def epc(self, today=True):
		if today:
			x = (Decimal(self.today) / self.clicks_today) if self.clicks_today > 0 else 0
		else:
			x = (Decimal(self.total) / self.clicks) if self.clicks > 0 else 0

		return format(float(x), ".2f").rstrip('0').rstrip('.')

	def output_dict(self):
		return {
			"clicks": {
				"today": self.clicks_today,
				"total": self.clicks
			},
			"conversions": {
				"today": self.conversions_today,
				"total": self.conversions
			},
			"earnings": {
				"today": currency(self.today),
				"week": currency(self.week),
				"month": currency(self.month),
				"year": currency(self.year),
				"total": currency(self.total)
			},
			"epc": {
				"today": self.epc()
			}
		}

	def reset_today(self):
		self.__class__.objects.filter(Q(clicks_today__gt=0) | Q(today__gt=0) | Q(yesterday__gt=0)) \
			.update(yesterday=F("today"), today=0, clicks_today=0, conversions_today=0)

	def reset_week(self):
		self.__class__.objects.filter(week__gt=0).update(week=0)

	def reset_month(self):
		self.__class__.objects.filter(Q(month__gt=0) | Q(yestermonth__gt=0)) \
			.update(yestermonth=F("month"), month=0)

	def reset_year(self):
		self.__class__.objects.filter(year__gt=0).update(year=0)

	def add(self, amount, cut=0):
		amount = Decimal(amount)
		amount_cut = amount - (amount * cut)
		
		self.conversions 		= F("conversions") + 1
		self.conversions_today 	= F("conversions_today") + 1

		self.today 	= F("today") 	+ amount_cut
		self.week 	= F("week") 	+ amount_cut
		self.month 	= F("month")	+ amount_cut
		self.year 	= F("year") 	+ amount_cut
		self.total 	= F("total") 	+ amount_cut

		self.save()
		return amount_cut

	def subtract(self, amount):
		amount = Decimal(amount)

		self.today 	= F("today") 	- amount
		self.week 	= F("week") 	- amount
		self.month 	= F("month")	- amount
		self.year 	= F("year") 	- amount
		self.total 	= F("total") 	- amount

		self.save()
		return amount

	def difference(self, amount, cut=0):
		return self.add(amount, 1 - cut)

	def __get_base_u(self, search_model, date_range, show_all=False):
		args = {}

		# Typeof would be "user" or "offer" [or even "token" (unnecessary)]
		model = str(type(self.obj).__name__).lower()

		# So if user in field_names then we know to add the model name to search args
		if model in ("user", "offer"):
			if model == "offer" and search_model.__name__.lower() == "token":
				args["offers__in"] = [self.obj.pk]

			else:
				args[model] = self.obj

		# otherwise we know it's a Locker
		else:
			args.update(self.obj.lookup_args())

		# Include date_range to queryset
		if date_range:
			args["datetime__range"] = date_range

		# Show every conversion, including conversion blocked ones
		if not show_all:
			args["blocked"] = False

		return search_model.objects.filter(**args)

	def __get_base(self, search_model, date_range, show_all=False):
		return self.__get_base_u(search_model, date_range, show_all).order_by("-datetime")

	def get_conversions_u(self, date_range=None, show_all=False):
		# Unordered
		return self.__get_base_u(conversions.models.Conversion, date_range, show_all)

	def get_conversions(self, date_range=None, show_all=False):
		return self.__get_base(conversions.models.Conversion, date_range, show_all)

	def get_conversions_today(self, show_all=False):
		return self.get_conversions((date.today(), date.today() + timedelta(days=1)), show_all)

	def get_tokens(self, date_range=None):
		return self.__get_base(conversions.models.Token, date_range, True)

	def get_tokens_today(self):
		return self.get_tokens((date.today(), date.today() + timedelta(days=1)))

	def get_viewers(self, minutes=5):
		return self.get_tokens((datetime.now() - timedelta(minutes=minutes), datetime.now())).count()

	def increment_clicks(self):
		self.clicks 		= F("clicks") 		+ 1
		self.clicks_today 	= F("clicks_today") + 1
		self.save()

	class Meta:
		abstract = True
		verbose_name = "Earnings"
		verbose_name_plural = "Earnings"


# Signals
from . import signals