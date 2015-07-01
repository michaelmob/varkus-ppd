from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User

from utils import strings
from geoip import lookup

from ..lockers.utils import Locker


class Token(models.Model):
	unique 		= models.CharField(max_length=32)
	data 		= models.CharField(max_length=200, default=None, blank=True, null=True)

	locker		= models.CharField(max_length=10, choices=settings.LOCKERS, default=None, blank=True, null=True)
	locker_id	= models.IntegerField(default=None, blank=True, null=True)
	locker_code	= models.CharField(max_length=10, default=None, blank=True, null=True)

	user_agent 	= models.CharField(max_length=300)
	ip_address 	= models.GenericIPAddressField()
	date_time	= models.DateTimeField()

	lead 		= models.BooleanField(default=False)
	paid 		= models.BooleanField(default=False)
	staff 		= models.BooleanField(default=False)

	def __str__(self):
		return "%s: %s" % (self.pk, self.unique)

	def locker_object(self):
		try:
			return Locker(self.locker).objects.get(id=self.locker_id)
		except:
			return None

	def get_or_create_request(request, locker_obj):
		return Token.get_or_create(
			request.META.get("REMOTE_ADDR"),
			request.META.get("HTTP_USER_AGENT"),
			locker_obj
		)

	def access(self):
		return (self.lead or self.paid or self.staff)

	def renew(self):
		cache.delete("token__" + self.unique)

	def get_or_create(ip_address, user_agent, locker_obj):
		locker = str(type(locker_obj).__name__).upper()

		token, created = Token.objects.get_or_create(
			ip_address 		= ip_address,
			user_agent 		= user_agent,
			locker 			= locker,
			locker_id		= locker_obj.id,
			locker_code		= locker_obj.code,
			defaults 		= {
				"unique": strings.random(32),
				"date_time": datetime.now()
			}
		)

		return token

	def get_verify(unique, ip_address):
		try:
			return Token.objects.get(unique=unique, ip_address=ip_address)
		except Token.DoesNotExist:
			return None

	def clear():
		return Token.objects.filter(
			date_time__lt = datetime.now() - timedelta(days=2),
			paid = False
		)


class Deposit(models.Model):
	user_id		= models.IntegerField()
	company		= models.CharField(max_length=32)
	aff_id		= models.IntegerField()
	code		= models.CharField(max_length=32)
	name		= models.CharField(max_length=32)
	password	= models.CharField(max_length=32)

	def initiate():
		Deposit.objects.all().delete()

		for deposit in settings.DEPOSITS:
			Deposit.objects.create(
				user_id		= deposit[0],
				company		= deposit[1],
				aff_id 		= deposit[2],
				code		= deposit[3],
				name		= deposit[4],
				password 	= deposit[5],
			)

	def get_by_user_id(user_id):
		try:
			return Deposit.objects.get(user_id=user_id)
		except:
			None

	def get_by_code(code):
		try:
			return Deposit.objects.get(code=code)
		except:
			None

	def get_by_password(password):
		try:
			return Deposit.objects.get(password=password)
		except:
			None


class Lead(models.Model):
	offer 				= models.ForeignKey("offers.Offer", default=None, blank=True, null=True)
	offer_name			= models.CharField(max_length=150, default=None, blank=True, null=True)
	country 			= models.CharField(max_length=2, default=None, blank=True, null=True)

	token 				= models.ForeignKey(Token, related_name="token_id", default=None, blank=True, null=True)
	user 				= models.ForeignKey(User, related_name="user_id", default=None, blank=True, null=True)

	locker				= models.CharField(max_length=10, choices=settings.LOCKERS, default=None, blank=True, null=True)
	locker_id			= models.IntegerField(default=None, blank=True, null=True)
	locker_code			= models.CharField(max_length=10, default=None, blank=True, null=True)

	sender_ip_address	= models.GenericIPAddressField(blank=True, null=True)
	user_ip_address		= models.GenericIPAddressField(blank=True, null=True)

	user_user_agent		= models.CharField(max_length=300, default=None, blank=True, null=True)

	payout				= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	dev_payout			= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	user_payout			= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	referral_payout		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)

	lead_blocked		= models.BooleanField(default=False)
	approved			= models.BooleanField(default=True)

	deposit				= models.CharField(max_length=32, default="DEFAULT_DEPOSIT", blank=True, null=True, choices=settings.DEPOSIT_NAMES)
	date_time			= models.DateTimeField()


	def locker_object(self):
		try:
			return Locker(self.locker).objects.get(id=self.locker_id)
		except:
			return None


	def create(
		offer,
		token,
		user,
		locker_obj,
		sender_ip_address,
		user_ip_address,
		payout,
		dev_payout,
		user_payout,
		referral_payout,
		deposit="DEFAULT_DEPOSIT",
		lead_blocked=False,
		approved=True
	):
		locker = str(type(locker_obj).__name__).upper()

		args = {
			"offer" 			: offer,
			"offer_name"		: offer.name,

			"token" 			: token,
			"user"				: user,
			"locker"			: locker,

			"sender_ip_address"	: sender_ip_address,
			"user_ip_address"	: user_ip_address,

			"user_user_agent" 	: token.user_agent,

			"payout"			: payout,
			"dev_payout"		: dev_payout,
			"user_payout"		: user_payout,
			"referral_payout"	: referral_payout,

			"lead_blocked"		: lead_blocked,
			"approved"			: approved,

			"deposit"			: deposit,
			"date_time"			: datetime.now(),
		}

		# locker_obj may not exist
		try:
			args["locker_id"] = locker_obj.id
			args["locker_code"] = locker_obj.code
		except:
			pass

		# Lookup throws error if inexistant
		try:
			args["country"] = lookup.country(user_ip_address)
		except:
			args["country"] = offer.flag

		return Lead.objects.create(**args)
