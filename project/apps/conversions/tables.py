from collections import defaultdict
import django_tables2 as tables

from django.conf import settings
from django.db.models import Count
from django.utils.safestring import mark_safe

from utils.country import COUNTRIES
from apps.offers.tables import Table_Offer_Base
from apps.offers.models import Offer
from .models import Conversion, Token

class Table_Conversions_Base(Table_Offer_Base):

	class Meta(Table_Offer_Base.Meta):
		model = Conversion
		fields = ()

	def data(self, **kwargs):
		return Conversion.objects.filter(**self.args) \
			.prefetch_related("locker", "offer").order_by("-datetime")

	def __init__(self, request, date_range=None,
		per_page=settings.ITEMS_PER_PAGE_LARGE, **kwargs):
		# Filter Args
		self.cut_amount = request.user.profile.party.cut_amount
		self.args = { "user": request.user }
		if date_range != None and date_range[0] != None:
			self.args["datetime__range"] = date_range

		# Create Table
		super(__class__, self).__init__(request, self.data(), per_page)


class Table_Conversions(Table_Conversions_Base):
	locker = tables.Column(verbose_name="Locker")
	approved = tables.Column(verbose_name="Status")

	class Meta(Table_Offer_Base.Meta):
		model = Conversion
		empty_text = "There doesn't seem to be any conversions here for this category or date range."
		fields = ("locker", "offer", "user_ip_address", "user_payout", "datetime", "approved")


class Table_Statistics_Base(Table_Conversions_Base):
	distinct_field = "offer_id"

	class Meta(Table_Conversions_Base.Meta):
		model = Conversion
		orderable = False
		empty_text = "There doesn't seem to be any conversions here for this category or date range."
		fields = ("clicks", "conversions")

	def __init__(self, request, date_range=None, per_page=2147483647, **kwargs):
		super(__class__, self).__init__(request, date_range, per_page, **kwargs)

	def foreach_token(self, tokens):
		for token in tokens:
			for offer in token.offers.all():
				# Add Click
				self.offers["clicks"][offer.id] += 1

	def foreach_conversion(self, conversions):
		for conversion in conversions:
			# Add Conversion
			self.offers["conversions"][conversion.offer_id] += 1

			# Add Chargeback
			if conversion.approved == False:
				self.offers["chargebacks"][conversion.offer_id] += 1

	def data(self, **kwargs):
		# Create class variable
		self.offers = {
			"clicks": defaultdict(int),
			"conversions": defaultdict(int),
			"chargebacks": defaultdict(int)
		}

		# Related Offer IDs
		#offer_ids = list(set([n[0] for n in data.values_list("offer_id")]))

		### CLICKS ###
		self.foreach_token(
			Token.objects.filter(**self.args).prefetch_related("offers")
		)

		### CONVERSIONS and CHARGEBACKS ###
		self.foreach_conversion(
			Conversion.objects.filter(**self.args)
		)

		return Conversion.objects.filter(**self.args).defer("locker") \
			.prefetch_related("offer").distinct(self.distinct_field)

	def render_clicks(self, record):
		return self.offers["clicks"].get(eval("record." + self.distinct_field), 0)

	def render_conversions(self, record):
		return self.offers["conversions"].get(eval("record." + self.distinct_field), 0)

	def render_chargebacks(self, record):
		return self.offers["chargebacks"].get(eval("record." + self.distinct_field), 0)


class Table_Statistics_Offers(Table_Statistics_Base):
	clicks = tables.Column(empty_values=())
	conversions = tables.Column(empty_values=())
	user_payout = tables.Column()
	chargebacks = tables.Column(empty_values=())

	class Meta(Table_Statistics_Base.Meta):
		fields = ("offer", "clicks", "conversions", "user_payout", "chargebacks")


class Table_Statistics_Countries(Table_Statistics_Base):
	clicks = tables.Column(empty_values=())
	conversions = tables.Column(empty_values=())
	chargebacks = tables.Column(empty_values=())

	distinct_field = "country"

	class Meta(Table_Statistics_Base.Meta):
		fields = ("country", "clicks", "conversions")

	def foreach_token(self, tokens):
		for token in tokens:
			self.offers["clicks"][token.country] += 1

	def foreach_conversion(self, conversions):
		for conversion in conversions:
			# Set uppercase just in case some are lower
			conversion.country = conversion.country.upper()

			# Add Conversion
			self.offers["conversions"][conversion.country] += 1

			# Add Chargeback
			if conversion.approved == False:
				self.offers["chargebacks"][conversion.country] += 1

	def render_country(self, value):
		return mark_safe("<i class='%s flag'></i>%s" % (
			value.lower(), COUNTRIES[value.upper()]))