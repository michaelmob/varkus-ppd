from decimal import Decimal, getcontext
from datetime import timedelta, date

from django.db import models, connection
from django.core.urlresolvers import reverse

import apps.leads
from apps.billing.models import Billing

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

	today		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	yesterday	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	week		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	month		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	yestermonth	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	year 		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	total		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)

	real_today 	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	real_month	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	real_total	= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	
	def reset_today(self):
		print("Reset Today")
		cursor = connection.cursor()
		cursor.execute(
			"UPDATE `%s` SET yesterday=today, today=0, real_today=0 WHERE today>0 OR yesterday>0" %
				(self._meta.db_table)
		)

	def reset_week(self):
		print("Reset Week")
		cursor = connection.cursor()
		cursor.execute(
			"UPDATE `%s` SET week=0 WHERE week>0" %
				(self._meta.db_table)
		)

	def reset_month(self):
		print("Reset Month")
		cursor = connection.cursor()
		cursor.execute(
			"UPDATE `%s` SET yestermonth=month, month=0, real_month=0 WHERE month>0 OR yestermonth>0" %
				(self._meta.db_table)
		)

	def reset_year(self):
		print("Reset Year")
		cursor = connection.cursor()
		cursor.execute(
			"UPDATE `%s` SET year=0 WHERE year>0" %
				(self._meta.db_table)
		)

	def add(self, amount, cut=0, add_to_real=True):
		getcontext().prec = 2
		amount = Decimal(amount)
		amount_cut = Decimal(amount - (amount * Decimal(cut)))

		self.leads 			+= 1

		self.today 			+= amount_cut
		self.week 			+= amount_cut
		self.month 			+= amount_cut
		self.year 			+= amount_cut
		self.total 			+= amount_cut

		if add_to_real:
			self.real_today 	+= amount
			self.real_month 	+= amount
			self.real_total 	+= amount

		self.save()
		return amount_cut

	def difference(self, amount, cut=0, add_to_real=False):
		return self.add(amount, 1 - cut, add_to_real)

	def get_leads(self, date_range=[date.today(), date.today() + timedelta(days=1)], count=2147483647, all=False):
		args = {}

		typeof = str(type(self.obj).__name__).lower()

		# User
		if typeof in apps.leads.models.Lead._meta.get_all_field_names():
			args[typeof] = self.obj
		
		# Locker
		else:
			args["locker"] = typeof.upper()
			args["locker_id"] = self.obj.pk
			args["locker_code"] = self.obj.code

		if date_range:
			args["date_time__range"] = date_range

		if not all:
			args["lead_blocked"] = False
			
		return apps.leads.models.Lead.objects.filter(**args).order_by("-date_time")[:count]

	def get_most_recent_leads(self, count=25):
		return self.get_leads(None, count)

	class Meta:
		abstract = True

