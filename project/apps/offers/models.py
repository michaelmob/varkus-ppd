import hashlib
from collections import OrderedDict

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django_countries import countries

from viking.utils.user_agent import format_user_agent
from viking.utils.constants import BLANK_NULL, CURRENCY

from core.models import EarningsBase
from conversions.deposits import Deposit
from .constants import CATEGORY_TYPES
from .utils.container import OfferDataContainer



class OfferQuerySet(models.QuerySet):
	"""
	QuerySet for Offer model.
	* Do not set class variables, they remain on each new request. *
	"""

	def for_request(self, request_or_container, locker_object=None):
		"""
		Chain to queryset to limit to viable offers.
		
		Either put a request or a container into the `request_or_container`
		parameter. If a container is put, leave `locker_object` as None.
		"""
		# Load container
		if type(request_or_container) == OfferDataContainer:
			container = request_or_container

		# Or create container
		else:
			container = OfferDataContainer(request_or_container, locker_object)

		# Be sure that container is valid
		if not container.is_valid:
			return self.none()

		# Results
		return (
			self
				.filter(*container.args, **container.kwargs)
				.exclude(id__in=container.block_ids())
				.exclude(id__in=container.exclude_ids())
				.exclude(id__in=container.object_ids)
		)



class OfferManager(models.Manager):
	"""
	Manager for the Offer model.
	"""

	def get_queryset(self):
		"""
		Returns QuerySet for the Offer model.
		"""
		return OfferQuerySet(self.model, using=self._db)


	def for_request(self, *args, **kwargs):
		"""
		Passthrough method for `for_request` method of the queryset.
		"""
		return self.get_queryset().for_request(*args, **kwargs)


	def get_offers(self, request, locker_object=None, count=10):
		"""
		Get offers that can be completed by the request.
		"""
		c = OfferDataContainer(request, locker_object, count)

		# Staff Priority and User Priority
		c.append(
			(
				(
					self.filter(priority=True) |
					self.filter(id__in=c.priority_ids()) |
					self.filter(id__in=c.boost_ids())
				)
				.for_request(c)
				.order_by("-priority", "-earnings_per_click"))
		)

		# Fill up with random
		c.append(
			self
				.for_request(c)
				.order_by("-earnings_per_click")
		)

		return c.result()



class Offer(models.Model):
	"""
	Model for Offer.
	"""

	offer_id	 	= models.IntegerField(null=True)
	priority 		= models.BooleanField(default=False)
	name 			= models.CharField(max_length=250, verbose_name="Name")
	anchor 			= models.CharField(max_length=1000, verbose_name="Anchor")
	requirements 	= models.CharField(max_length=1000, verbose_name="Requirements")
	user_agent 		= models.CharField(max_length=50, default="", verbose_name="User Agent", **BLANK_NULL)
	category		= models.CharField(max_length=50, choices=CATEGORY_TYPES, verbose_name="Category", **BLANK_NULL)
	countries 		= models.CharField(max_length=747)
	country			= models.CharField(max_length=5)
	country_count 	= models.IntegerField()
	payout 			= models.DecimalField(verbose_name="Payout", **CURRENCY)
	earnings_per_click = models.DecimalField(verbose_name="EPC", **CURRENCY)
	success_rate	= models.FloatField(verbose_name="Success Rate")
	tracking_url 	= models.CharField(max_length=1000)
	date 			= models.DateField(auto_now_add=True)

	objects 		= OfferManager()
	

	def __str__(self):
		"""
		String value for object.
		"""
		return "%s: %s" % (self.pk, self.name)


	def save(self, *args, **kwargs):
		"""
		Override .save() method to modify/clean various fields and create a
		related earnings object if non-existant.
		Returns updated Offer object.
		"""
		self.name = self.clean_name()
		self.country = self.choose_country()
		self.user_agent = format_user_agent(self.user_agent)
		self.country_count = len(self.countries.split(","))
		self.success_rate = float(self.payout) - float(self.earnings_per_click)

		super(__class__, self).save(*args, **kwargs)

		if not hasattr(self, "earnings"):
			Earnings.objects.create(parent=self)


	def get_absolute_url(self):
		"""
		Returns detail view for Offer object.
		"""
		return reverse("offers:detail", args=(self.pk,))


	def get_redirect_url(self, locker_object):
		"""
		locker_object (object) -> Locker object.
		Returns redrect view for Offer object.
		"""
		return reverse(locker_object.type + ":redirect", args=(locker_object.code, self.pk))


	def get_tracking_url(self, offer, token):
		"""
		Returns formatted tracking URL.
		"""
		try:
			affiliate_id = Deposit.get_by_user_id(token.user.pk).affiliate_id
		except:
			affiliate_id = Deposit.default_affiliate_id()

		return (
			str(offer.tracking_url)
				.replace("{o}", str(offer.offer_id))
				.replace("{a}", str(affiliate_id))
				.replace("{u}", str(token.unique))
		)


	def clean_name(self):
		"""
		Returns cleaned name of Offer object.
		"""
		self.name = str(self.name).split('(')[0]

		if self.name.endswith("- "):
			self.name = (self.name[:-2]).strip()

		return self.name


	def choose_country(self):
		"""
		Chooses most relevant flag for Offer object. If greater than 10
		countries use "INTL", otherwise "US" if less than 10 and contains "US".
		Returns ISO-Alpha-2 country code.
		"""
		countries = self.countries.upper().split(',')
		count = len(countries)

		# Less than 10 countries and US is in the country list
		if count < 10 and "US" in countries:
			self.country = "US"

		# More than 10 countries or country is "-"
		elif count > 10 or countries == "-":
			self.country = "INTL"

		# Choose first country's code
		else:
			self.country = countries[0]

		return self.country


	def get_countries(self):
		"""
		Returns list of countries.
		"""
		return self.countries.split(",")


	def get_country(self):
		"""
		Returns country name from country code.
		"""
		if self.country == "INTL":
			return "International"
		return dict(countries)[self.country.upper()]



class Earnings(EarningsBase):
	"""
	Earnings model for Offers.
	"""

	parent = models.OneToOneField(Offer, primary_key=True)

	class Meta:
		verbose_name_plural = "Earnings"