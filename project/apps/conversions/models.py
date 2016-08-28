from decimal import Decimal
from datetime import datetime, timedelta
from random import randint
from utils import strings
from utils.constants import (DEFAULT_BLANK_NULL, BLANK_NULL, CURRENCY,
	USER_AGENTS)
from utils.geoip import country_code

from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
	datetime	= models.DateTimeField()
	last_access	= models.DateTimeField(auto_now_add=True, verbose_name="Last Access")

	conversion 	= models.BooleanField(default=False, verbose_name="Conversion")


	def __str__(self):
		return "%s: %s" % (self.pk, self.unique)


	def create_random(obj, offer=None, date=None):
		""" Generate random Token (for debugging purposes) """
		country = "XX"

		# Random, but valid, IP Address and country
		while country == "XX":
			ip_address = ".".join(str(randint(0, 255)) for n in range(4))
			try:
				country = country_code(ip_address)
			except:
				country = "XX"

		# Random Date
		if not date:
			date = datetime.now().replace(hour=randint(0, 23), minute=randint(0, 59))

		# Create the actual token
		token = Token.objects.create(
			ip_address 	= ip_address,
			locker 		= obj,
			user_agent 	= USER_AGENTS[randint(0, len(USER_AGENTS) - 1)],
			user 		= obj.user,
			country 	= country,
			unique 		= strings.random(64),
			session 	= None,
			datetime 	= date
		)

		# Random offer
		if not offer:
			offer = apps.offers.models.Offer.objects.filter(
				earnings_per_click__gt=0.01
			).order_by("?").first()

		# Add offer
		if offer:
			token.offers.add(offer)

		# Increment clicks
		try:
			offer.earnings.increment_clicks()
			obj.user.earnings.increment_clicks()
			obj.earnings.increment_clicks()
		except:
			pass

		return token


	def get(request, obj):
		"""Get token by identifiers

		request -- Get User's IP Address and User Agent
		obj -- Locker object to create for
		"""
		return Token.objects.filter(
			ip_address = request.META.get("REMOTE_ADDR"),
			**obj.lookup_args()
		).first()


	def get_or_create(request, obj):
		"""Get or create token

		request -- http request
		obj -- Locker object to create for
		"""
		country = country_code(
			(request.META.get("REMOTE_ADDR").upper()
				if request.META.get("REMOTE_ADDR") != "127.0.0.1"
				else "173.63.97.160")
		)
		
		if not country:
			country = "XX"

		# Create Session
		if not request.session.exists(request.session.session_key):
			request.session.create()

		token = Token.get(request, obj)
		created = False

		if not token:
			token = Token.objects.create(
				ip_address 	= request.META.get("REMOTE_ADDR"),
				locker 		= obj,
				user_agent 	= request.META.get("HTTP_USER_AGENT"),
				user 		= obj.user,
				country 	= country,
				unique 		= strings.random(64),
				session 	= request.session.session_key,
				datetime 	= datetime.now())
			created = True

		if not created:
			if token.session != request.session.session_key:
				token.session = request.session.session_key
				token.save()

		return (token, created)


	def access(self):
		"""Check if token has access to continue"""
		return self.conversion


	def clear():
		"""Clear/delete all tokens"""
		return Token.objects.filter(
			datetime__gt=datetime.now() - timedelta(days=31)
		).delete()



class Conversion(models.Model):
	offer 				= models.ForeignKey("offers.Offer", verbose_name="Offer", on_delete=models.SET_NULL, **DEFAULT_BLANK_NULL)
	offer_name			= models.CharField(max_length=150, verbose_name="Offer Name", **DEFAULT_BLANK_NULL)
	country 			= models.CharField(max_length=3, verbose_name="Country", **DEFAULT_BLANK_NULL)

	token 				= models.ForeignKey(Token, verbose_name="Token", related_name="token_id", on_delete=models.SET_NULL, **DEFAULT_BLANK_NULL)
	user 				= models.ForeignKey(User, verbose_name="User", related_name="user_id", on_delete=models.SET_NULL, **DEFAULT_BLANK_NULL)

	locker_type 		= models.ForeignKey(ContentType, on_delete=models.SET_NULL, limit_choices_to={"app_label__in": ("lockers",)}, **BLANK_NULL)
	locker_id 			= models.PositiveIntegerField(**BLANK_NULL)
	locker 				= GenericForeignKey("locker_type", "locker_id")

	access_url 			= models.CharField(verbose_name="Access URL", max_length=850, **DEFAULT_BLANK_NULL)
	sender_ip_address	= models.GenericIPAddressField(verbose_name="Sender IP Address", **BLANK_NULL)
	user_ip_address		= models.GenericIPAddressField(verbose_name="IP Address", **BLANK_NULL)

	user_user_agent		= models.CharField(verbose_name="User-Agent", max_length=300, **DEFAULT_BLANK_NULL)

	payout				= models.DecimalField(verbose_name="Total Payout", **CURRENCY)
	dev_payout			= models.DecimalField(verbose_name="Dev Payout", **CURRENCY)
	user_payout			= models.DecimalField(verbose_name="Payout", **CURRENCY)
	referral_payout		= models.DecimalField(verbose_name="Referral Payout", **CURRENCY)

	blocked				= models.BooleanField(verbose_name="Blocked", default=False)
	approved			= models.BooleanField(verbose_name="Approved", default=True)

	deposit				= models.CharField(max_length=32, default="DEFAULT_DEPOSIT", choices=Deposit.names(), **BLANK_NULL)
	seconds 			= models.IntegerField(default=0)
	datetime			= models.DateTimeField(verbose_name="Date")

	
	def time_to_complete(self):
		""" Time it took for the offer to be completed """
		if 0 > self.seconds > 1800:
			return "Unknown"

		d = datetime(1, 1, 1) + timedelta(seconds=self.seconds)
		return "{}m {}s".format(d.minute, d.second)


	def get_or_create(token, offer=None, sender=None, payout=None,
		deposit="DEFAULT_DEPOSIT", blocked=False, approved=True, **kwargs):
		""" Create Conversion """
		# Last offer from token
		if token and not offer:
			offer = token.offers.last()

		# Still no offer? Just make one for the sake of it
		if not offer:
			offer = apps.offers.models.Offer()

		# Create blank token if no token
		if not token:
			token = Token()

		# Values to search for existing Conversion
		search = {
			"offer" 	: offer if offer.pk else None,
			"token"		: token if token.pk else None,
			"user"		: token.user,
		}

		# Attempt to find an existing conversion
		obj = Conversion.objects.filter(**search).first()

		if obj:
			return (obj, False)

		_datetime = datetime.now()
		seconds = int((_datetime - token.last_access).total_seconds())

		# Conversion does not exist
		# Creation values for conversion
		values = {
			"locker"			: token.locker,
			"offer_name"		: offer.name,
			"sender_ip_address"	: sender,
			"user_ip_address"	: token.ip_address,
			"user_user_agent" 	: token.user_agent,
			"payout"			: Decimal(payout or offer.payout), 
			"blocked"			: blocked,
			"approved"			: approved,
			"deposit"			: deposit,
			"datetime" 			: _datetime,
			"seconds" 			: seconds
		}

		# Datetime optional
		if "datetime" in kwargs:
			if kwargs["datetime"] == "TOKEN":
				values["datetime"] = token.datetime.replace(
					minute=randint(token.datetime.minute, 59),
					second=randint(token.datetime.second, 59),
				)
			else:
				values["datetime"] = kwargs["datetime"]

		# Find IP address country, use Offer's country if not found
		values["country"] = country_code(token.ip_address)

		if not values["country"]:
			values["country"] = offer.flag

		# Add the original `search` values to `values`
		values.update(search)
		
		# Create the conversion
		return (Conversion.objects.create(**values), True)


# Signals
from . import signals