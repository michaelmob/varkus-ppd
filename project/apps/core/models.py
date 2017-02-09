import json
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.apps import apps
from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import User
from viking.utils.constants import CURRENCY, BLANK_NULL
from core.templatetags.currency import currency



class EarningsBase(models.Model):
	"""
	Abstract model Earnings for any object that uses an Earnings class.
	"""
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


	class Meta:
		abstract = True
		verbose_name = "Earnings"
		verbose_name_plural = "Earnings"


	@classmethod
	def run_reset(cls, time_period):
		"""
		Reset earnings based on time period.
		"""
		# Daily reset
		if time_period == "today":
			return (
				cls.objects
					.filter(Q(clicks_today__gt=0) | Q(today__gt=0) | Q(yesterday__gt=0))
					.update(yesterday=F("today"), today=0, clicks_today=0, conversions_today=0)
			)

		# Week reset
		if time_period == "week":
			return cls.objects.filter(week__gt=0).update(week=0)

		# Month reset
		if time_period == "month":
			return (
				cls.objects
					.filter(Q(month__gt=0) | Q(yestermonth__gt=0))
					.update(yestermonth=F("month"), month=0)
			)

		# Year reset
		if time_period == "year":
			return cls.objects.filter(year__gt=0).update(year=0)


	def earnings_per_click(self, today=True):
		"""
		Returns earnings per click for object.
		"""
		if today:
			a, b = self.today, self.clicks_today
		else:
			a, b = self.total, self.clicks

		x = Decimal(a) / b if b > 0 else 0
		return format(float(x), ".2f").rstrip('0').rstrip('.')


	def output_dict(self):
		"""
		Returns object's earning details as a dictionary.
		"""
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
				"today": self.earnings_per_click()
			}
		}


	def add(self, conversion, field="payout"):
		"""
		Add earnings to object's earnings.
		Returns the calculated amount minus the taken cut.
		"""
		if hasattr(conversion, "do_not_add"):
			return

		amount = Decimal(getattr(conversion, field))
		today = datetime.today()
		
		# Same day
		if conversion.datetime.date() == today.date():
			self.conversions_today = F("conversions_today") + 1
			self.today = F("today") + amount

		# Same week
		if conversion.datetime.strftime("%W") == today.strftime("%W"):
			self.week = F("week") + amount

		# Same month
		if conversion.datetime.month == today.month:
			self.month = F("month") + amount

		# Same year
		if conversion.datetime.year == today.year:
			self.year = F("year") + amount

		self.conversions = F("conversions") + 1
		self.total = F("total") + amount
		self.save()
		return amount


	def remove(self, conversion, field="payout"):
		"""
		Subtract earnings from object's earnings.
		Returns the amount subtracted.
		"""
		amount = Decimal(getattr(conversion, field))
		today = datetime.today()

		# Same day
		if conversion.datetime.date() == today.date():
			self.conversions_today = F("conversions_today") - 1
			self.today = F("today") - amount

		# Same week
		if conversion.datetime.strftime("%W") == today.strftime("%W"):
			self.week = F("week") - amount

		# Same month
		if conversion.datetime.month == today.month:
			self.month = F("month") - amount

		# Same year
		if conversion.datetime.year == today.year:
			self.year = F("year") - amount

		self.conversions = F("conversions") - 1
		self.total = F("total") - amount
		self.save()
		return amount


	def get_related(self, search_model, **kwargs):
		"""
		Returns queryset of related objects from specified model.
		"""
		# Type would be 'user' or 'offer' or even 'token'
		parent_model_name = str(type(self.parent).__name__).lower()
		search_model_name = search_model.__name__.lower()


		# Parent model of 'user' or 'offer' would mean 
		if parent_model_name in ("user", "offer"):
			# Offer; offers__in = [1]
			if parent_model_name == "offer" and search_model_name == "token":
				kwargs["offers__in"] = [self.parent.pk]

			# User; user = 1
			else:
				kwargs[parent_model_name] = self.parent

		# otherwise we know it's a Locker
		else:
			kwargs.update(self.parent.filter_args())

		# Only show blocked conversions when explicitly specified
		if search_model_name == "conversion":
			kwargs["is_blocked"] = kwargs.get("is_blocked", False)

		return search_model.objects.filter(**kwargs)


	def get_conversions(self, **kwargs):
		"""
		Return Conversions related to object.
		"""
		model = apps.get_model("conversions", "Conversion")
		return self.get_related(model, **kwargs)


	def get_conversions_today(self, **kwargs):
		"""
		Return Conversions related to object with date range of Today.
		"""
		today = date.today()
		return self.get_conversions(
			datetime__range=(today, today + timedelta(days=1))
		)


	def get_tokens(self, date_range=None, **kwargs):
		"""
		Return Tokens related to object.
		"""
		model = apps.get_model("conversions", "Token")
		return self.get_related(model, **kwargs)


	def get_tokens_today(self, **kwargs):
		"""
		Return Tokens related to object with date range of Today.
		"""
		today = date.today()
		return self.get_tokens(
			datetime__range=(today, today + timedelta(days=1))
		)


	def increment_clicks(self):
		"""
		Increment a click on earnings object.
		"""
		self.clicks = F("clicks") + 1
		self.clicks_today = F("clicks_today") + 1
		self.save()