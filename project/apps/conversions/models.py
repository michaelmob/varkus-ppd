from datetime import datetime, timedelta
from viking.utils.constants import DEFAULT_BLANK_NULL, BLANK_NULL, CURRENCY

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from . import managers
from .deposits import Deposit



class Token(models.Model):
	"""
	Model for Token table.
	"""
	objects 	= managers.TokenManager()

	unique 		= models.CharField(max_length=64, unique=True)
	session 	= models.CharField(max_length=64, **BLANK_NULL)
	data 		= models.CharField(max_length=200, **DEFAULT_BLANK_NULL)

	user 		= models.ForeignKey(User, on_delete=models.SET_NULL, **DEFAULT_BLANK_NULL)
	offers 		= models.ManyToManyField("offers.Offer", related_name="token_offer_id", verbose_name="Offer", default=None, blank=True)

	locker_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, limit_choices_to={"app_label__in": ("lockers",)}, **BLANK_NULL)
	locker_id 	= models.PositiveIntegerField(**BLANK_NULL)
	locker 		= GenericForeignKey("locker_type", "locker_id")

	user_agent 	= models.CharField(max_length=300)
	ip_address 	= models.GenericIPAddressField(verbose_name="IP Address")
	country 	= models.CharField(max_length=5, **DEFAULT_BLANK_NULL)
	datetime	= models.DateTimeField(auto_now_add=True)
	last_access	= models.DateTimeField(auto_now_add=True, verbose_name="Last Access")

	conversion 	= models.BooleanField(default=False, verbose_name="Conversion")


	def __str__(self):
		return "%s: %s" % (self.pk, self.unique)


	@property
	def has_access(self):
		"""
		Token has access to the locker object's result.
		"""
		return self.conversion



class Conversion(models.Model):
	"""
	Model for Conversion table.
	"""
	objects 			= managers.ConversionManager()

	offer 				= models.ForeignKey("offers.Offer", verbose_name="Offer", on_delete=models.SET_NULL, **DEFAULT_BLANK_NULL)
	offer_name			= models.CharField(max_length=150, verbose_name="Offer Name", **DEFAULT_BLANK_NULL)
	country 			= models.CharField(max_length=3, verbose_name="Country", **DEFAULT_BLANK_NULL)

	token 				= models.ForeignKey(Token, verbose_name="Token", related_name="token_id", on_delete=models.SET_NULL, **DEFAULT_BLANK_NULL)
	user 				= models.ForeignKey(User, verbose_name="User", related_name="user_id", on_delete=models.SET_NULL, **DEFAULT_BLANK_NULL)

	locker_type 		= models.ForeignKey(ContentType, on_delete=models.SET_NULL, limit_choices_to={"app_label__in": ("lockers",)}, **BLANK_NULL)
	locker_id 			= models.PositiveIntegerField(**BLANK_NULL)
	locker 				= GenericForeignKey("locker_type", "locker_id")

	access_url 			= models.CharField(verbose_name="Access URL", max_length=850, **DEFAULT_BLANK_NULL)
	accessor_ip_address	= models.GenericIPAddressField(verbose_name="Accessor IP Address", **BLANK_NULL)
	ip_address			= models.GenericIPAddressField(verbose_name="IP Address", **BLANK_NULL)

	user_agent			= models.CharField(verbose_name="User-Agent", max_length=300, **DEFAULT_BLANK_NULL)

	payout				= models.DecimalField(verbose_name="Payout", **CURRENCY)
	dev_payout			= models.DecimalField(verbose_name="Dev Payout", **CURRENCY)
	referral_payout		= models.DecimalField(verbose_name="Referral Payout", **CURRENCY)
	total_payout		= models.DecimalField(verbose_name="Total Payout", **CURRENCY)

	is_blocked			= models.BooleanField(verbose_name="Blocked", default=False)
	is_approved			= models.BooleanField(verbose_name="Approved", default=True)

	deposit				= models.CharField(max_length=32, default="DEFAULT_DEPOSIT", choices=Deposit.names(), **BLANK_NULL)
	seconds 			= models.IntegerField(default=0)
	datetime			= models.DateTimeField(verbose_name="Date")

	
	@property
	def time_to_complete(self):
		"""
		Returns humanized value for `seconds` field.
		"""
		if 0 > self.seconds > 1800:
			return "Unknown"

		d = datetime(1, 1, 1) + timedelta(seconds=self.seconds)
		return "{}m {}s".format(d.minute, d.second)



class Boost(models.Model):
	"""
	Model for Boost table.
	"""
	objects 	= managers.BoostManager()

	user 	= models.ForeignKey(User, verbose_name="User")
	offer 	= models.ForeignKey("offers.Offer", verbose_name="Offer")
	count 	= models.PositiveIntegerField(default=0)


	def decrement_clicks(self):
		"""
		Decrement 1 from count.
		"""
		self.count = models.F("count") - 1
		self.save()