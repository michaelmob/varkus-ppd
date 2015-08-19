from decimal import Decimal, getcontext
from datetime import datetime, date, timedelta

from django.db import models, connection
from django.core.urlresolvers import reverse
from django.core.cache import cache

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

	clicks		= models.IntegerField(default=0)
	clicks_hourly = models.CharField(default="", max_length=250)

	def reset_today(self):
		print("Reset Today's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE `%s` SET yesterday=today, today=0, real_today=0 WHERE today>0 OR yesterday>0" % (self._meta.db_table))
		cursor.execute("UPDATE `%s` SET clicks_hourly='' WHERE LENGTH(clicks_hourly)>1" % (self._meta.db_table))

	def reset_week(self):
		print("Reset Week's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE `%s` SET week=0 WHERE week>0" % (self._meta.db_table))

	def reset_month(self):
		print("Reset Month's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE `%s` SET yestermonth=month, month=0, real_month=0 WHERE month>0 OR yestermonth>0" % (self._meta.db_table))

	def reset_year(self):
		print("Reset Year's Earnings")
		cursor = connection.cursor()
		cursor.execute("UPDATE `%s` SET year=0 WHERE year>0" % (self._meta.db_table))

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

	def __add_click_hour(self, string, hour, number):
		string = string.split(',')
		str_len = len(string)

		if(hour > str_len):
			string.extend([str(0) for x in range(hour - str_len + 1)])
		elif(hour == str_len):
			string.append(str(0))

		string[hour] = str(number)

		return ','.join(string)

	def increment_clicks(self, ip_address):
		""" Add click if unique """
		key = "c_%s_%s" % (self._meta.db_table, self.pk)
		clicks = cache.get(key)

		# Cache array not created, create array
		if not clicks:
			clicks = []

		# IP is in cached array so it's not unique
		elif ip_address in clicks:
			return False

		# If 25 IPs in array then remove one
		# and add the new one
		if(len(clicks) >= 25):
			clicks.pop(0)

		clicks.append(ip_address)
		cache.set(key, clicks, 300)

		# Add to total count
		# Add click to hourly clicks
		self.count += 1
		self.hourly = self.__add_click_hour(self.hourly, datetime.now().hour, self.count)
		self.save()

		return True

	class Meta:
		abstract = True

