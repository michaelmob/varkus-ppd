import hashlib

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
	
	user 		= models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL)
	offer 		= models.ForeignKey("offers.Offer", related_name="token_offer_id", verbose_name="Offer", default=None, blank=True, null=True, on_delete=models.SET_NULL)

	locker		= models.CharField(max_length=10, choices=settings.LOCKERS, default=None, blank=True, null=True)
	locker_id	= models.IntegerField(default=None, blank=True, null=True)
	locker_code	= models.CharField(max_length=10, default=None, blank=True, null=True)

	user_agent 	= models.CharField(max_length=300)
	ip_address 	= models.GenericIPAddressField()
	country 	= models.CharField(max_length=5)
	date_time	= models.DateTimeField()
	last_access	= models.DateTimeField(auto_now=True)

	lead 		= models.BooleanField(default=False)
	paid 		= models.BooleanField(default=False)
	staff 		= models.BooleanField(default=False)

	def __str__(self):
		return "%s: %s" % (self.pk, self.unique)

	def locker_object(self):
		"""Get Locker object from Token"""
		try:
			return Locker(self.locker).objects.get(id=self.locker_id)
		except:
			return None

	def _get(ip_address, user_agent, locker_obj):
		"""Get token by identifiers

		ip_address -- User's IP Address
		user_agent -- User's User Agent
		locker_obj -- Locker object to create for
		"""
		locker = str(type(locker_obj).__name__).upper()

		return Token.objects.get(
			ip_address 		= ip_address,
			user_agent 		= user_agent,
			locker 			= locker,
			locker_id		= locker_obj.id,
			locker_code		= locker_obj.code,
		)

	def get(request, locker_obj):
		"""Get token using _get method

		request -- django request
		locker_obj -- Locker object to get for
		"""
		return Token._get(
			request.META.get("REMOTE_ADDR"),
			request.META.get("HTTP_USER_AGENT"),
			locker_obj
		)

	def _get_or_create(ip_address, user_agent, locker_obj):
		"""Get or create token

		ip_address -- User's IP Address
		user_agent -- User's User Agent
		locker_obj -- Locker object to create for
		"""
		locker = str(type(locker_obj).__name__).upper()

		return Token.objects.get_or_create(
			ip_address 		= ip_address,
			user_agent 		= user_agent,
			country 		= lookup.country(ip_address),
			user 			= locker_obj.user,
			locker 			= locker,
			locker_id		= locker_obj.id,
			locker_code		= locker_obj.code,
			defaults 		= {
				"unique": strings.random(32),
				"date_time": datetime.now()
			}
		)

	def get_or_create(request, locker_obj):
		"""Get or create token from request

		request -- Django request to get IP Address and User Agent from
		locker_obj -- Locker object to create for
		"""
		return Token._get_or_create(
			request.META.get("REMOTE_ADDR"),
			request.META.get("HTTP_USER_AGENT"),
			locker_obj
		)

	def access(self):
		"""Check if token has access to continue"""
		return (self.lead or self.paid or self.staff)

	def renew(request):
		return cache.delete("o_%s_%s" % \
			(
				self.ip_address,
				hashlib.sha256(self.user_agent.encode("utf-8")).hexdigest()
			)
		)

	def get_verify(unique, ip_address):
		"""Verify token for unique and ip_address exists by returning the object"""
		try:
			return Token.objects.get(unique=unique, ip_address=ip_address)
		except Token.DoesNotExist:
			return None

	def clear():
		"""Clear/delete all tokens"""
		return Token.objects.filter(
			date_time__gt = datetime.now() - timedelta(days=2),
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
	offer 				= models.ForeignKey("offers.Offer", verbose_name="Offer", default=None, blank=True, null=True, on_delete=models.SET_NULL)
	offer_name			= models.CharField(max_length=150, verbose_name="Offer", default=None, blank=True, null=True)
	country 			= models.CharField(max_length=2, verbose_name="Country", default=None, blank=True, null=True)

	token 				= models.ForeignKey(Token, verbose_name="Token", related_name="token_id", default=None, blank=True, null=True, on_delete=models.SET_NULL)
	user 				= models.ForeignKey(User, verbose_name="User", related_name="user_id", default=None, blank=True, null=True, on_delete=models.SET_NULL)

	locker				= models.CharField(verbose_name="Locker", max_length=10, choices=settings.LOCKERS, default=None, blank=True, null=True)
	locker_id			= models.IntegerField(verbose_name="Locker ID", default=None, blank=True, null=True)
	locker_code			= models.CharField(verbose_name="Locker Code", max_length=10, default=None, blank=True, null=True)

	access_url 			= models.CharField(verbose_name="Access URL", max_length=850, default=None, blank=True, null=True)
	sender_ip_address	= models.GenericIPAddressField(verbose_name="Sender IP Address", blank=True, null=True)
	user_ip_address		= models.GenericIPAddressField(verbose_name="IP Address", blank=True, null=True)

	user_user_agent		= models.CharField(verbose_name="User-Agent", max_length=300, default=None, blank=True, null=True)

	payout				= models.DecimalField(verbose_name="Total Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)
	dev_payout			= models.DecimalField(verbose_name="Dev Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)
	user_payout			= models.DecimalField(verbose_name="Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)
	referral_payout		= models.DecimalField(verbose_name="Referral Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)

	lead_blocked		= models.BooleanField(verbose_name="Lead Blocked", default=False)
	approved			= models.BooleanField(verbose_name="Approved", default=True)

	deposit				= models.CharField(max_length=32, default="DEFAULT_DEPOSIT", blank=True, null=True, choices=settings.DEPOSIT_NAMES)
	date_time			= models.DateTimeField(verbose_name="Date", auto_now_add=True)

	def locker_object(self):
		try:
			return Locker(self.locker).objects.get(id=self.locker_id)
		except:
			return None

	def create(
		offer, token, user, locker_obj, sender_ip_address, user_ip_address,
		payout, dev_payout, user_payout, referral_payout, deposit="DEFAULT_DEPOSIT",
		access_url="", lead_blocked=False, approved=True
	):
		locker = str(type(locker_obj).__name__).upper()

		try:
			user_agent = token.user_agent
		except:
			user_agent = ""

		args = {
			"offer" 			: offer,
			"offer_name"		: offer.name,

			"token" 			: token,
			"user"				: user,
			"locker"			: locker,

			"access_url"		: access_url,
			"sender_ip_address"	: sender_ip_address,
			"user_ip_address"	: user_ip_address,

			"user_user_agent" 	: user_agent,

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
