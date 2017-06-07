from django_tables2.utils import A

from django.conf import settings
from django.utils.html import format_html
from django.core.urlresolvers import reverse

from .models import Offer
from conversions.models import Conversion
from core.tables import tables, TableBase



class OfferTableBase(TableBase):
	"""
	Base class for tables that displays offers
	"""
	cut_amount = 1


	def render_locker(self, value, record):
		"""
		Render locker object as 'Locker: Name'
		"""
		locker = record.locker
		return format_html(
			"{}: <a href=\"{}\">{}</a>",
			locker.type.title(), locker.get_absolute_url(), locker.name
		)


	def render_earnings_per_click(self, value):
		"""
		Render earnings_per_click with a cut amount
		"""
		return self.currency(value, self.cut_amount)


	def render_payout(self, value):
		"""
		Render payout with a cut amount
		"""
		return self.currency(value, self.cut_amount)


	def render_country(self, value, record):
		"""
		Render flag with varying 'x more'
		"""
		value = value.lower()

		if value == "intl":
			value = "world icon"

		result = self.flag(value)

		if record.country_count > 1:
			result += format_html("<small>{} more</small>", record.country_count - 1)

		return result


	def render_approved(self, record):
		"""
		Render approved column with a colored label
		"""
		if record.is_approved:
			color, text = ("green", "Approved")
		else:
			color, text = ("red", "Chargeback")

		return format_html(
			"<span class=\"ui {} horizontal label\">{}</span>", color, text
		)


	def render_ip_address(self, value, record):
		"""
		Render IP Address with its country's flag
		"""
		return self.flag(record.country) + format_html("{}", value)


	def render_success_rate(self, value):
		"""
		Render success rate of an offer with a percent sign
		"""
		return "%.3g%%" % value



class OfferTable(OfferTableBase):
	"""
	Table that displays offers
	"""
	name = tables.LinkColumn("offers:detail", verbose_name="Offer", args=(A("pk"),))
	boost = tables.Column(empty_values=(), verbose_name="")


	class Meta(OfferTableBase.Meta):
		model = Conversion
		empty_text = "No offers matching your search exist."
		fields = (
			"name", "category", "country", "user_agent", "earnings_per_click",
			"payout", 
		)


	def render_name(self, value, record):
		"""
		Returns boost button.
		"""
		return format_html(
			"<a data-id='{}' class='ui horizontal orange label boost'>"
				"<i class='rocket icon'></i>"
			"</a>"

			"<a href='{}'>{}</a>",
			
			record.pk, reverse("offers:detail", args=(record.pk,)), record.name
		)


class OfferConversionsTable(OfferTableBase):
	"""
	Table that displays conversions of an offer
	"""
	ttc = tables.Column(accessor="time_to_complete", verbose_name="TTC", orderable=False)


	class Meta(OfferTableBase.Meta):
		model = Conversion
		empty_text = "You haven't received any conversions with this offer."
		fields = ("ip_address", "payout", "ttc", "datetime")
		exclude = ("offer",)


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