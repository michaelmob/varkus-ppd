import json
from decimal import Decimal, getcontext
from datetime import datetime, date, timedelta

from django.db import models, connection
from django.db.models import F
from django.core.urlresolvers import reverse
from django.core.cache import cache

import apps.conversions as conversions

getcontext().prec = 2


class Earnings_Base(models.Model):
	clicks			= models.IntegerField(default=0, verbose_name="Clicks")
	conversions		= models.IntegerField(default=0)

	clicks_today	= models.IntegerField(default=0, verbose_name="Today's Clicks")
	conversions_today = models.IntegerField(default=0, verbose_name="Today's Conversions")

	today			= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Today")
	yesterday		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Yesterday")
	week			= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Week")
	month			= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Month")
	yestermonth		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Last Month")
	year 			= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Year")
	total			= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Total")

	real_today 		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="*Today")
	real_month		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="*Month")
	real_total		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="*Total")

	def epc(self, today=True):
		if today:
			return (Decimal(self.today) / self.clicks_today) if self.clicks_today > 0 else 0
		else:
			return (Decimal(self.total) / self.clicks) if self.clicks > 0 else 0

	def reset_today(self):
		print("Reset Today's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE %s SET yesterday=today, today=0, real_today=0, clicks_today=0, conversions_today=0 WHERE clicks_today>0 OR today>0 OR yesterday>0" % (self._meta.db_table))

	def reset_week(self):
		print("Reset Week's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE %s SET week=0 WHERE week>0" % (self._meta.db_table))

	def reset_month(self):
		print("Reset Month's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE %s SET yestermonth=month, month=0, real_month=0 WHERE month>0 OR yestermonth>0" % (self._meta.db_table))

	def reset_year(self):
		print("Reset Year's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE %s SET year=0 WHERE year>0" % (self._meta.db_table))

	def add(self, amount, cut=0, add_to_real=True):
		amount = Decimal(amount)
		amount_cut = Decimal(amount - (amount * Decimal(cut)))

		self.conversions 		= F("conversions") + 1
		self.conversions_today 	= F("conversions_today") + 1

		self.today 	= F("today") 	+ amount_cut
		self.week 	= F("week") 	+ amount_cut
		self.month 	= F("month")	+ amount_cut
		self.year 	= F("year") 	+ amount_cut
		self.total 	= F("total") 	+ amount_cut

		if add_to_real:
			self.real_today = F("real_today") + amount
			self.real_month = F("real_month") + amount
			self.real_total = F("real_total") + amount

		self.save()
		return amount_cut

	def difference(self, amount, cut=0, add_to_real=False):
		return self.add(amount, 1 - cut, add_to_real)

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
			args["locker"] = self.obj

		# Include date_range to queryset
		if date_range:
			args["date_time__range"] = date_range

		# Show every conversion, including conversion blocked ones
		if not show_all:
			args["conversion_blocked"] = False

		return search_model.objects.filter(**args)

	def __get_base(self, search_model, date_range, show_all=False):
		return self.__get_base_u(search_model, date_range, show_all).order_by("-date_time")

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
