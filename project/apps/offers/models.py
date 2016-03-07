import hashlib

from decimal import Decimal
from datetime import date, datetime, timedelta
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.gis.geoip2 import GeoIP2

from ..cp.models import Earnings_Base
from ..leads.models import Lead, Token

from django_countries import countries as _countries
from utils.user_agent import get_ua


class Offer(models.Model):
	offer_id	 			= models.IntegerField()
	priority 				= models.BooleanField(default=False)
	name 					= models.CharField(max_length=250, verbose_name="Name")
	anchor 					= models.CharField(max_length=1000, verbose_name="Anchor")
	requirements 			= models.CharField(max_length=1000, verbose_name="Requirements")
	user_agent 				= models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="User Agent")
	category				= models.CharField(max_length=50, choices=settings.CATEGORY_TYPES, blank=True, null=True, verbose_name="Category")
	earnings_per_click 		= models.DecimalField(max_digits=15, decimal_places=2, verbose_name="EPC")
	country 				= models.CharField(max_length=747)
	flag 					= models.CharField(max_length=5, verbose_name="Country")
	country_count 			= models.IntegerField()
	payout 					= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Payout")
	success_rate			= models.FloatField(verbose_name="Success Rate")
	tracking_url 			= models.CharField(max_length=1000)
	date 					= models.DateField(auto_now_add=True)

	def __str__(self):
		return "%s: %s" % (self.pk, self.name)

	def get_manage_url(self):
		try:
			return reverse("offers-manage", args=(self.pk,))
		except:
			return "#"

	def get_by_offer_id(offer_id):
		""" Get offer by its id from the ad company """
		try:
			return Offer.objects.get(offer_id=offer_id)
		except Offer.DoesNotExist:
			return None

	def pick_flag(country):
		""" Picks the flag for the offer, if it above 10 then
			use intl, otherwise US if under 10 with US in it """
		country = country.lower().split(',')
		count = len(country)
		result = None

		# Less than 10 countries and US is in the country list
		if (count < 10) and ("us" in country):
			result = "us"

		# More than 10 countries or country is "-"
		elif (count > 10) or (country == "-"):
			result = "intl"

		else:
			result = country[0]

		return result

	def clean_name(dirty):
		""" Clean the name from the useless shit
			that the ad company gives """

		dirty = str(dirty).split('(')[0]

		if dirty.endswith("- "):
			dirty = (dirty[:-2]).strip()

		return dirty

	def create(
		id, name, anchor, requirements, user_agent, category,
		earnings_per_click, country, payout, tracking_url
	):
		""" Create offer with arguments """
		obj = Offer.objects.create(
			offer_id				= id,
			name					= Offer.clean_name(name),
			anchor					= anchor,
			requirements			= requirements,
			user_agent				= user_agent,
			category				= category,
			earnings_per_click 		= Decimal(earnings_per_click),
			country 				= country,
			flag 					= str(Offer.pick_flag(country)).upper(),
			country_count 			= len(country.split(',')),
			payout 					= payout,
			difference				= payout - Decimal(earnings_per_click),
			tracking_url 			= tracking_url)

		# Create Earnings Object
		Earnings.objects.get_or_create(obj=obj)

		return obj

	def get(request, obj):
		""" Get offers by locker object """
		profile = obj.user.profile

		return Offer._get(
			request.META.get("REMOTE_ADDR"), request.META.get("HTTP_USER_AGENT"),
			obj.offers_count if 0 < obj.offers_count < 51 else settings.OFFERS_COUNT,
			0.01, profile.offer_priority, profile.offer_block)

	def get_cache(request, obj):
		""" Get offers by using the request to retrieve cached offers,
			if there are no cached offers then fetch new ones... serve
			from cache (this is the one you want to use from a view)
			[call offer item .renew() to renew cached offers] """

		# Make key for cache
		key = "o_%s_%s_%s" % (
			request.META.get("REMOTE_ADDR"),
			hashlib.sha256(request.META.get("HTTP_USER_AGENT").encode("utf-8")).hexdigest(),
			obj.code)

		# Get Offers
		offers = cache.get(key)

		# If no offers then get and set them
		if not offers:
			offers = Offer.get(request, obj)
			cache.set(key, offers, 120)  # Cache for 2 minutes

		return offers

	def renew(request):
		return cache.delete("o_%s_%s" % (
			request.META.get("REMOTE_ADDR"),
			hashlib.sha256(request.META.get("HTTP_USER_AGENT").encode("utf-8")).hexdigest()))

	def get_basic(
		count, category, country, user_agent=None, min_payout=0.01,
		offer_block=[], offer_exclude=[], filters={}
	):
		""" Get offers with a bunch of customizable arguments """

		args = (Q(user_agent=None),)

		if user_agent:
			args = (Q(user_agent__icontains=user_agent) | Q(user_agent=None),)

		return Offer.objects\
			.filter(
				category__in 		= category,
				payout__gte 		= min_payout,
				country__icontains 	= country,
				success_rate__gte 	= 3,
				**filters
			)\
			.exclude(pk__in=offer_block)\
			.exclude(pk__in=offer_exclude)\
			.order_by("-earnings_per_click")[:count]

	def random(
		count, country, user_agent=None, min_payout=0.01,
		offer_block=None, offer_exclude=[]
	):
		""" Get offers randomly """

		return Offer.objects.all()\
			.filter(
				payout__gte 		= min_payout,
				country__icontains 	= country,
				success_rate__gte 	= 3,
				user_agent			= ""
			)\
			.exclude(pk__in=offer_block)\
			.exclude(pk__in=offer_exclude)\
			.order_by("?")[:count]

	def _get(
		ip_address, user_agent, count=5, min_payout=0.01,
		offer_priority=None, offer_block=None
	):
		""" Get offers with ip_address and user_agent,
			geoip tells what country the ip_address is
			of and selects specific offers with user_agents
			that correspond to given user_agent """

		user_agent = get_ua(user_agent)

		offer_block = [o.id for o in offer_block.all()] if offer_block else []
		offer_priority = [o.id for o in offer_priority.all()] if offer_priority else []

		# GeoIP
		try:
			data = GeoIP2().city(ip_address if ip_address != "127.0.0.1" else "173.63.97.160")
		except:
			data = {"country_code": "xx", "city": "Unknown"}

		country, region = (data["country_code"], data["city"])

		_offers = []

		# Block Completed Offers
		leads = Lead.objects\
			.filter(
				user_ip_address = ip_address,
				date_time__gt 	= datetime.now() - timedelta(hours=6)
			)

		for lead in leads:
			offer_block.append(lead.offer.id)

		# User Agent Args
		args = (Q(user_agent=None),)
		if user_agent:
			args = (
				Q(user_agent__icontains=user_agent) |
				Q(user_agent=None),
			)

		# Staff Priority
		_offers += Offer.objects\
			.filter(
				priority 			= True,
				payout__gte 		= min_payout,
				country__icontains 	= country,
				*args
			)\
			.exclude(pk__in=offer_block)

		# User Priority
		_offers += Offer.objects\
			.filter(
				pk__in 				= offer_priority,
				payout__gte 		= min_payout,
				country__icontains 	= country,
				*args
			)

		# Common arguments
		kwargs = {
			"country": country,
			"offer_block": offer_block,
			"min_payout": min_payout,
			"user_agent": user_agent,
			"offer_exclude": [_offer.pk for _offer in _offers]
		}

		_30 = int(0.3 * count)
		_20 = int(0.2 * count)

		# Android _offers
		if user_agent == "Android":
			_offers += Offer.get_basic(_30, ["Android", "Mobile"], **kwargs)

		# iPhone _offers
		elif user_agent == "iPhone":
			_offers += Offer.get_basic(_30, ["iPhone", "iOS Devices", "Mobile"], **kwargs)

		# iPad _offers
		elif user_agent == "iPad":
			_offers += Offer.get_basic(_30, ["iPad", "iOS Devices", "Mobile"], **kwargs)

		# We'll assume it's Windows
		elif user_agent == "Windows":
			_offers += Offer.get_basic(_30, ["Downloads"], **kwargs)

		# Email _offers
		_offers += Offer.get_basic(_30, ["Email Submits"], **kwargs)

		# PIN _offers
		_offers += Offer.get_basic(_20, ["PIN Submit"], **kwargs)

		# Update _offers in common arguments for no duplicates
		kwargs["offer_exclude"] = [offer.pk for offer in _offers]

		# Fill rest of spaces with random surveys
		if len(_offers) < count:
			_offers += Offer.random(count - len(_offers), **kwargs)

		# Replace {region} with region
		for offer in _offers:
			if "{region}" in offer.anchor:
				offer.anchor = offer.anchor.replace("{region}", region)

		return _offers[:count]

	def get_countries(self):
		""" Countries Dictionary """
		countries = dict(_countries)
		result = {}

		for country in self.country.upper().split(","):
			if country in countries:
				result[country] = countries[country]

		return result

	def get_country(self):
		""" Get country name from code """

		if self.flag == "intl":
			return "International"

		return dict(_countries)[self.flag.upper()]


class Earnings(Earnings_Base):
	obj = models.OneToOneField(Offer, primary_key=True)

	class Meta:
		verbose_name_plural = "Earnings"
