import django_tables2 as tables

from django.utils.html import format_html
from django.db.models import Count, Sum, Case, When, IntegerField
from django.urls import reverse

from viking.utils.country import COUNTRIES
from offers.tables import OfferTableBase
from core.tables import CurrencyColumn
from .models import Conversion, Token



class ConversionsTableBase(OfferTableBase):
	"""
	Table base for any Conversions table
	"""
	offer = tables.LinkColumn("offers:detail", text=lambda r: r.offer_name, args=(tables.A("offer.id"),), empty_values=())
	ttc = tables.Column(verbose_name="TTC", accessor="time_to_complete", order_by=("seconds",))


	class Meta(OfferTableBase.Meta):
		model = Conversion
		empty_text = "There doesn't seem to be any conversions here for this category or date range."
		fields = ()


	def get_queryset(args):
		"""
		Returns queryset for table.
		"""
		return (
			Conversion.objects
				.filter(**args)
				.prefetch_related("locker", "offer")
				.order_by("-datetime")
		)


	def render_offer(self, value, record):
		"""
		Cannot use LinkColumn because default text is forced. 
		Returns offer or offer_name if offer object does not exist.
		"""
		if value is None:
			return record.offer_name

		return format_html(
			"<a href=\"{url}\">{text}</a>",
			url=record.offer.get_absolute_url(),
			text=record.offer_name
		)


	def render_payout(self, value, record):
		"""
		Return payout; if unapproved, render a chargeback label.
		"""
		if not record.is_approved:
			return format_html(
				"<span class=\"ui red horizontal label\">Chargeback</span>"
			)

		return self.currency(value, self.cut_amount)



class ConversionsTable(ConversionsTableBase):
	"""
	Conversions table
	"""
	locker = tables.Column(verbose_name="Locker", accessor="locker_type")


	class Meta(ConversionsTableBase.Meta):
		fields = ("locker", "offer", "ip_address", "payout", "ttc", "datetime")



class StatisticsTableBase(ConversionsTableBase):
	"""
	Table base for any statistics table
	"""
	distinct_field = None


	class Meta(ConversionsTableBase.Meta):
		orderable = False
		fields = ("clicks", "conversions")


	@classmethod
	def get_queryset(cls, args):
		"""
		Returns queryset for table.
		"""
		objects = (
			Conversion.objects
				.filter(**args)
				.prefetch_related("locker", "offer")
				.distinct(cls.distinct_field)
				.exclude(**{cls.distinct_field: None})
		)

		# Allow modifications of queryset through modify_queryset() method
		return cls.modify_queryset(objects)


	@classmethod
	def modify_queryset(cls, objects):
		"""
		Add conversions, chargebacks, and earnings to conversion objects.
		Returns modified queryset.
		"""
		# Get conversion and chargebacks count
		conversions = (
			Conversion.objects
				.only(cls.distinct_field, "payout", "is_approved")
				.values(cls.distinct_field)
				.annotate(
					earnings=Sum("payout"),
					conversions=Count(cls.distinct_field),
					chargebacks=Sum(
						Case(When(is_approved=False, then=1), output_field=IntegerField())
					)
				)
		)

		# Format data into a dict we can index for offer id
		data = {
			obj[cls.distinct_field]: (
				obj["conversions"] or 0,
				obj["chargebacks"] or 0,
				obj["earnings"] or 0
			) for obj in conversions if obj[cls.distinct_field]
		}

		# Get all tokens attached to conversions
		tokens = list(
			Token.objects
				.filter(offers__in=objects.values_list("id", flat=True))
				.only("offers")
				.values_list("offers__id", flat=True)
		)

		# Loop through each object in objects and add data to it
		for obj in objects:
			obj.clicks = tokens.count(obj.id)
			field = obj.__dict__[cls.distinct_field]
			
			if not field:
				continue

			obj.conversions = data[field][0]  # 0 is conversions
			obj.chargebacks = data[field][1]  # 1 is chargebacks
			obj.earnings = data[field][2]	  # 2 is earnings

		return objects



class OfferStatisticsTable(StatisticsTableBase):
	"""
	Statistics for Offers
	"""
	clicks = tables.Column()
	chargebacks = tables.Column()
	earnings = CurrencyColumn(accessor="earnings")

	distinct_field = "offer_id"


	class Meta(StatisticsTableBase.Meta):
		model = None
		fields = ("offer",)
		exclude = ("ttc",)



class CountryStatisticsTable(StatisticsTableBase):
	"""
	Statistics for Countries
	"""
	country = tables.Column()
	clicks = tables.Column()
	chargebacks = tables.Column()
	earnings = CurrencyColumn(accessor="earnings")

	distinct_field = "country"


	class Meta(StatisticsTableBase.Meta):
		model = None
		fields = ("country",)
		exclude = ("offer", "ttc",)


	def render_country(self, value):
		"""
		Return country flag as 'i' element.
		"""
		return format_html(
			"<i class=\"{} flag\"></i>{}",
			value.lower(), COUNTRIES[value.upper()]
		)