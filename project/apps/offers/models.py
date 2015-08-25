from decimal import Decimal
from datetime import date, datetime, timedelta

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.cache import cache

from django_countries import countries

from ..cp.models import Earnings_Base
from ..leads.models import Lead, Token

from celery import shared_task
from geoip import lookup
from utils.user_agent import get_ua


class Offer(models.Model):
	offer_id	 			= models.IntegerField()
	priority 				= models.BooleanField(default=False)
	name 					= models.CharField(max_length=150, verbose_name="Name")
	anchor 					= models.CharField(max_length=500, verbose_name="Anchor")
	requirements 			= models.CharField(max_length=500, verbose_name="Requirements")
	user_agent 				= models.CharField(max_length=50, default="", blank=True, verbose_name="User Agent")
	category				= models.CharField(max_length=50, choices=settings.CATEGORY_TYPES, blank=True, null=True, verbose_name="Category")
	earnings_per_click 		= models.DecimalField(max_digits=15, decimal_places=2, verbose_name="EPC")
	country 				= models.CharField(max_length=747)
	flag 					= models.CharField(max_length=3, verbose_name="Country")
	country_count 			= models.IntegerField()
	payout 					= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2, verbose_name="Payout")
	difference				= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)
	tracking_url 			= models.CharField(max_length=300)
	date 					= models.DateField()

	def __str__(self):
		return "%s: %s" % (self.pk, self.name)

	def get_by_offer_id(offer_id):
		""" Get offer by its id from the ad company """
		try:
			return Offer.objects.get(offer_id=offer_id)
		except Offer.DoesNotExist:
			return None

	def pick_flag(country):
		""" Picks the flag for the offer, if it above 10 then
			use intl, otherwise US if under 10 with US in it """
		countries = country.lower().split(',')
		count = len(countries)

		if (count < 10) and ("us" in country):
			return "us"
		elif (count > 10) or (country == "-"):
			return "intl"
		elif (count == 1):
			return country
		else:
			return countries[0]

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
			user_agent				= user_agent if user_agent else "",
			category				= category,
			earnings_per_click 		= Decimal(earnings_per_click),
			country 				= country,
			flag 					= str(Offer.pick_flag(country)).upper(),
			country_count 			= len(country.split(',')),
			payout 					= payout,
			difference				= payout - Decimal(earnings_per_click),
			tracking_url 			= tracking_url,
			date 					= date.today()
		)

		# Create Earnings Object
		Earnings.objects.get_or_create(obj=obj)

		return obj

	def offers_request(
		request, count=5, min_payout=0.01,
		offer_priority=None, offer_block=None
	):
		""" Get offers by request only """
		return Offer.get(
			request.META.get("REMOTE_ADDR"), request.META.get("HTTP_USER_AGENT"),
			count, min_payout, offer_priority, offer_block
		)

	def get_locker_request(request, locker_obj, count=5, min_payout=0.01):
		""" Get offers by locker object """
		user = locker_obj.user.profile
		return Offer.offers_request(
			request, count, min_payout, user.offer_priority, user.offer_block
		)

	def get_locker_request_cache(request, locker_obj, count=5, min_payout=0.01):
		""" Get offers by using the request to retrieve the token,
			user_agent, and user. then if already retrieved... serve
			from cache (this is the one you want to use from a view)
			[call token item .renew() its cached offers] """

		token = Token.get_or_create_request(request, locker_obj).unique

		# Get Offers
		offers = cache.get("t_" + token)

		# If no offers then get and set them
		if not offers:
			offers = Offer.get_locker_request(
				request, locker_obj, count, min_payout)

			cache.set("t_" + token, offers, 300)  # Cache for 5 minutes
			
		return Combo(offers, token)

	def get_basic_ex(
		count, category, country, user_agent=None, min_payout=0.01,
		offer_block=[], offer_exclude=[], extra={}
	):
		""" Get offers with a bunch of customizable arguments """

		args = (Q(user_agent=""),)

		if user_agent:
			args = (
				Q(user_agent__icontains=user_agent) |
				Q(user_agent=""),
			)
		
		return Offer.objects\
			.filter(
				category__in 		= category,
				payout__gte 		= min_payout,
				country__icontains 	= country,
				difference__lte 	= 3,
				*args,
				**extra
			)\
			.exclude(pk__in=offer_block)\
			.exclude(pk__in=offer_exclude)\
			.order_by("-earnings_per_click")[:count]
		
	def get_basic(
		count, category, country, user_agent=None, min_payout=0.01,
		offer_block=[], offer_exclude=[]
	):
		""" Get offers without extra arguments """
		return Offer.get_basic_ex(
			count, [category], country, user_agent,
			min_payout, offer_block, offer_exclude
		)
			
	def get_random(
		count, country, user_agent=None, min_payout=0.01,
		offer_block=None, offer_exclude=[]
	):
		""" Get offers randomly """
		args = (Q(user_agent=""),)

		if user_agent:
			args = (
				Q(user_agent__icontains=user_agent) |
				Q(user_agent=""),
			)
			
		return Offer.objects\
			.filter(
				payout__gte 		= min_payout,
				country__icontains 	= country,
				difference__lte 	= 3,
				*args
			)\
			.exclude(pk__in=offer_block)\
			.exclude(pk__in=offer_exclude)\
			.order_by("?")[:count]

	def get(
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
		
		c_r = lookup.country_region(
			ip_address if ip_address != "127.0.0.1" else "173.63.97.160"
		)

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
		args = (Q(user_agent=""),)
		if user_agent:
			args = (
				Q(user_agent__icontains=user_agent) |
				Q(user_agent=""),
			)
		
		# Staff Priority
		_offers += Offer.objects\
			.filter(
				priority 			= True,
				payout__gte 		= min_payout,
				country__icontains 	= c_r[0],
				*args
			)\
			.exclude(pk__in=offer_block)
			
		# User Priority
		_offers += Offer.objects\
			.filter(
				pk__in 				= offer_priority,
				payout__gte 		= min_payout,
				country__icontains 	= c_r[0],
				*args
			)
			
		# Common arguments
		kwargs = {
			"country": c_r[0],
			"offer_block": offer_block,
			"min_payout": min_payout,
			"user_agent": user_agent,
			"offer_exclude": [_offer.pk for _offer in _offers]
		}

		_30 = int(0.3 * count)
		_20 = int(0.2 * count)

		# Android _offers
		if user_agent == "Android":
			_offers += Offer.get_basic(_30, "Android", **kwargs)
			
		# iPhone _offers
		elif user_agent == "iPhone":
			_offers += Offer.get_basic_ex(_30, ["iPhone", "iOS Devices"], **kwargs)
			
		# iPad _offers
		elif user_agent == "iPad":
			_offers += Offer.get_basic_ex(_30, ["iPad", "iOS Devices"], **kwargs)
			
		# We'll assume it's Windows
		elif user_agent == "Windows":
			_offers += Offer.get_basic(_30, "Downloads", **kwargs)
		
		# Email _offers
		_offers += Offer.get_basic(_30, "Email Submits", **kwargs)

		# PIN _offers
		_offers += Offer.get_basic(_20, "PIN Submit", **kwargs)
		
		# Update _offers in common arguments for no duplicates
		kwargs["offer_exclude"] = [offer.pk for offer in _offers]
		
		# Fill rest of spaces with random surveys
		if len(_offers) < count:
			_offers += Offer.get_random(count - len(_offers), **kwargs)
			
		# Replace {region} with region
		for offer in _offers:
			if "{region}" in offer.anchor:
				offer.anchor = offer.anchor.replace("{region}", c_r[1])

		return _offers[:count]

	def get_countries(self):
		""" Countries to List """

		d = dict(countries)
		r = {}

		for c in self.country.split(","):
			try:
				r[c] = d[c]
			except:
				pass

		return r

	def get_country(self):
		""" Get country name from code """

		if self.flag == "intl":
			return "International"

		return dict(countries)[self.flag]
	

class Earnings(Earnings_Base):
	obj = models.OneToOneField(Offer, primary_key=True)

	class Meta:
		verbose_name_plural = "Earnings"


class Combo(object):

	def __init__(self, offers, token):
		super(Combo, self).__init__()
		self.offers = offers
		self.token = token
