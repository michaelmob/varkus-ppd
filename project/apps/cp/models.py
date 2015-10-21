import json
from decimal import Decimal, getcontext
from datetime import datetime, date, timedelta

from django.db import models, connection
from django.db.models import F
from django.core.urlresolvers import reverse
from django.core.cache import cache

import apps.leads
from apps.billing.models import Billing

getcontext().prec = 2

class Information(models.Model):
	key 	= models.CharField(max_length=1000, blank=True, null=True, default=None)
	value 	= models.CharField(max_length=1000, blank=True, null=True, default=None)

	def create(key, value):
		return Information.objects.create(
			key=key,
			value=value
		)

	def set(key, value):
		obj, created = Information.objects.get_or_create(key=key, defaults={"value": value})

		if not created:
			obj.value = value
			obj.save()

		return obj

	def remove(key):
		try:
			return Information.objects.get(key).delete()
		except:
			return False

	def has_add_permission(self, request):
		return False


class Earnings_Base(models.Model):
	leads		= models.IntegerField(default=0)
	clicks		= models.IntegerField(default=0, verbose_name="Clicks")

	today		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Today")
	yesterday	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Yesterday")
	week		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Week")
	month		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Month")
	yestermonth	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Last Month")
	year 		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Year")
	total		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Total")

	real_today 	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="*Today")
	real_month	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="*Month")
	real_total	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="*Total")


	def reset_today(self):
		print("Reset Today's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE %s SET yesterday=today, today=0, real_today=0 WHERE today>0 OR yesterday>0" % (self._meta.db_table))

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

		self.leads 	= F("leads") 	+ 1

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

	def __get_base(self, search_model, date_range=[date.today(), date.today() + timedelta(days=1)], count=None, every=False):
		args = {}

		# Typeof would be "user" or "offer" [or even "token" (unnecessary)]
		model = str(type(self.obj).__name__).lower()

		# So if user in field_names then we know to add the model name to search args
		if model in ["user", "offer"]:
			args[model] = self.obj

		# otherwise we know it's a Locker
		else:
			args["locker"] = model.upper()
			args["locker_id"] = self.obj.pk
			args["locker_code"] = self.obj.code

		if date_range:
			args["date_time__range"] = date_range

		if not all:
			args["lead_blocked"] = False

		if count:
			return search_model.objects.filter(**args).order_by("-date_time")[:count]
		else:
			return search_model.objects.filter(**args).order_by("-date_time")

	def get_leads(self, date_range=[date.today(), date.today() + timedelta(days=1)], count=None, every=False):
		return self.__get_base(apps.leads.models.Lead, date_range, count, every)

	def get_tokens(self, date_range=[date.today(), date.today() + timedelta(days=1)], count=None):
		return self.__get_base(apps.leads.models.Token, date_range, count, True)

	def get_most_recent_leads(self, count=25):
		return self.get_leads(None, count)

	def increment(self):
		self.clicks += 1
		self.save()

	class Meta:
		abstract = True
