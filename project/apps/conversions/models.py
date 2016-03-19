import hashlib
from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2

from utils import strings
from ..lockers.fields import LockerField

import apps.offers.models

class Deposit():
	user_id		= None
	company		= None
	aff_id		= None
	code		= None
	name		= None
	password	= None

	def search(column, value):
		result = None

		for deposit in settings.DEPOSITS:
			if deposit[column] == value:
				result = deposit

		if not result:
			result = settings.DEPOSITS[0]

		deposit	= Deposit()
		deposit.user_id 	= result[0]
		deposit.company 	= result[1]
		deposit.aff_id 		= result[2]
		deposit.code 		= result[3]
		deposit.name 		= result[4]
		deposit.password 	= result[5]

		return deposit

	def names():
		""" List all deposit names """
		return ((d[3], d[4]) for d in settings.DEPOSITS)

	def default_aff_id():
		""" Default affiliate ID """
		return settings.DEPOSITS[0][2]

	def default_password():
		""" Default postback password """
		return settings.DEPOSITS[0][5]

	def get_by_user_id(user_id):
		""" Get Deposit object by User's ID """
		return Deposit.search(0, user_id)

	def get_by_code(code):
		""" Get Deposit object by deposits code (DEFAULT_DEPOSIT) """
		return Deposit.search(3, code)

	def get_by_password(password):
		""" Get Deposit object by deposits password """
		return Deposit.search(5, password)


class Token(models.Model):
	unique 		= models.CharField(max_length=64, unique=True)
	session 	= models.CharField(max_length=64, null=True, blank=True)
	data 		= models.CharField(max_length=200, default=None, blank=True, null=True)

	user 		= models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL)
	offers 		= models.ManyToManyField("offers.Offer", related_name="token_offer_id", verbose_name="Offer", default=None, blank=True)

	locker 		= LockerField()

	user_agent 	= models.CharField(max_length=300)
	ip_address 	= models.GenericIPAddressField(verbose_name="IP Address")
	country 	= models.CharField(max_length=5)
	date_time	= models.DateTimeField()
	last_access	= models.DateTimeField(auto_now=True, verbose_name="Last Access")

	conversion 	= models.BooleanField(default=False, verbose_name="Conversion")
	paid 		= models.BooleanField(default=False)
	staff 		= models.BooleanField(default=False)

	def __str__(self):
		return "%s: %s" % (self.pk, self.unique)

	def get(request, obj):
		"""Get token by identifiers

		request -- Get User's IP Address and User Agent
		obj -- Locker object to create for
		"""
		try:
			return Token.objects.get(
				ip_address 		= request.META.get("REMOTE_ADDR"),
				#user_agent 	= request.META.get("HTTP_USER_AGENT"),
				locker 			= obj
			)
		except Token.DoesNotExist:
			return None

	def get_or_create(request, obj):
		"""Get or create token

		request -- http request
		obj -- Locker object to create for
		"""
		try:
			country = GeoIP2().country_code(request.META.get("REMOTE_ADDR") if request.META.get("REMOTE_ADDR") != "127.0.0.1" else "173.63.97.160")
		except:
			country = "xx"

		# Create Session
		if not request.session.exists(request.session.session_key):
			request.session.create()

		token, created = Token.objects.get_or_create(
			ip_address 		= request.META.get("REMOTE_ADDR"),
			locker 			= obj,
			defaults 		= {
				"user_agent": request.META.get("HTTP_USER_AGENT"),
				"user": obj.user,
				"country": country,
				"unique": strings.random(64),
				"session": request.session.session_key,
				"date_time": datetime.now()
			}
		)

		if not created:
			if token.session != request.session.session_key:
				token.session = request.session.session_key
				token.save()

		return (token, created)

	def access(self):
		"""Check if token has access to continue"""
		return (self.conversion or self.paid or self.staff)

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


class Conversion(models.Model):
	offer 				= models.ForeignKey("offers.Offer", verbose_name="Offer", default=None, blank=True, null=True, on_delete=models.SET_NULL)
	offer_name			= models.CharField(max_length=150, verbose_name="Offer Name", default=None, blank=True, null=True)
	country 			= models.CharField(max_length=3, verbose_name="Country", default=None, blank=True, null=True)

	token 				= models.ForeignKey(Token, verbose_name="Token", related_name="token_id", default=None, blank=True, null=True, on_delete=models.SET_NULL)
	user 				= models.ForeignKey(User, verbose_name="User", related_name="user_id", default=None, blank=True, null=True, on_delete=models.SET_NULL)

	locker				= LockerField()

	access_url 			= models.CharField(verbose_name="Access URL", max_length=850, default=None, blank=True, null=True)
	sender_ip_address	= models.GenericIPAddressField(verbose_name="Sender IP Address", blank=True, null=True)
	user_ip_address		= models.GenericIPAddressField(verbose_name="IP Address", blank=True, null=True)

	user_user_agent		= models.CharField(verbose_name="User-Agent", max_length=300, default=None, blank=True, null=True)

	payout				= models.DecimalField(verbose_name="Total Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)
	dev_payout			= models.DecimalField(verbose_name="Dev Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)
	user_payout			= models.DecimalField(verbose_name="Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)
	referral_payout		= models.DecimalField(verbose_name="Referral Payout", default=Decimal(0.00), max_digits=10, decimal_places=2)

	blocked				= models.BooleanField(verbose_name="Blocked", default=False)
	approved			= models.BooleanField(verbose_name="Approved", default=True)

	deposit				= models.CharField(max_length=32, default="DEFAULT_DEPOSIT", blank=True, null=True, choices=Deposit.names())
	date_time			= models.DateTimeField(verbose_name="Date", auto_now_add=True)


	def get_or_create(offer, token, payout, sender_ip_address, user_ip_address,
		deposit="DEFAULT_DEPOSIT", blocked=False, approved=True):
		""" Create Conversion Row """
		if not offer:
			offer = apps.offers.models.Offer()

		if not token:
			token = Token()

		args = {
			"offer" 			: offer if offer.pk else None,
			"token" 			: token if token.pk else None,
			"user"				: token.user,
			"locker"			: token.locker,
		}

		defaults = {
			"offer_name"		: offer.name,
			"sender_ip_address"	: sender_ip_address,
			"user_ip_address"	: user_ip_address,
			"user_user_agent" 	: token.user_agent,
			"payout"			: payout,
			"blocked"			: blocked,
			"approved"			: approved,
			"deposit"			: deposit,
			"date_time"			: datetime.now(),
		}

		# Find IP address country, use Offer's country if not found
		try:
			defaults["country"] = GeoIP2().country_code(user_ip_address)
		except:
			defaults["country"] = offer.flag

		return Conversion.objects.get_or_create(defaults=defaults, **args)


# Signals
from . import signals