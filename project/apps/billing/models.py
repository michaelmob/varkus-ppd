import json
from datetime import date, timedelta
from calendar import monthrange
from decimal import Decimal
from django.db import models
from django.db.models import Q, Sum
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from viking.utils.constants import CURRENCY, DEFAULT_BLANK_NULL, BLANK_NULL
from conversions.models import Conversion
from users.models import Profile
from .constants import PAYMENT_CHOICES
from . import managers



class Billing(models.Model):
	"""
	Billing profile for a User.
	"""
	user = models.OneToOneField(User, primary_key=True)
	choice = models.CharField(
		max_length=15, default="NONE", choices=PAYMENT_CHOICES
	)
	frequency = models.IntegerField(default=15)
	pending_earnings = models.DecimalField(**CURRENCY)
	paid_earnings = models.DecimalField(**CURRENCY)
	data = JSONField(default=dict, **BLANK_NULL)


	def save(self, *args, **kwargs):
		"""
		Change data to an empty dict if it is None.
		"""
		if self.data == None:
			self.data = {}
		return super(__class__, self).save(*args, **kwargs)


	def get_data(self):
		"""
		Return 'data' field as a dictionary.
		"""
		return json.loads(self.data)


	def get_earnings_sum(self, month_range, field="payout"):
		"""
		Returns sum of User's earnings.
		"""
		return (
			self.user.earnings
				.get_conversions(datetime__range=month_range)
				.aggregate(sum=Sum(field))["sum"]
		) or 0


	def get_referral_earnings_sum(self, month_range, field="referral_payout"):
		"""
		Returns sum of the User referral's earnings.
		"""
		users = Profile.objects.filter(referrer_id=self.user_id)
		if not users.exists():
			return 0

		return (
			Conversion.objects
				.filter(
					user__in=users.values_list("user_id"),
					datetime__range=month_range
				)
				.aggregate(sum=Sum(field))["sum"]
		) or 0



class Invoice(models.Model):
	"""
	Model for invoices.
	"""
	objects = managers.InvoiceManager()

	user = models.ForeignKey(User)
	creation_date = models.DateField(verbose_name="Creation Date")
	due_date = models.DateField(verbose_name="Due Date")
	period_start_date = models.DateField()
	period_end_date = models.DateField()
	total_amount = models.DecimalField(verbose_name="Total Amount", **CURRENCY)
	referral_amount = models.DecimalField(**CURRENCY)
	paid = models.BooleanField(default=False)
	error = models.BooleanField(default=False)
	notes = models.TextField(max_length=1000, default="", **BLANK_NULL)
	file = models.FileField(upload_to="billing/%Y/%m/", **DEFAULT_BLANK_NULL)