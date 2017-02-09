import django_tables2 as tables

from django.utils.timesince import timesince
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from conversions.models import Conversion
from core.tables import TableBase
from offers.tables import OfferTableBase, OfferTable



class SmallOffersTable(OfferTable):
	"""
	Non-detailed Offers table.
	"""

	class Meta(OfferTable.Meta):
		orderable = False
		attrs = {"class": "ui table"}
		fields = ("name", "country", "earnings_per_click", "payout")
		exclude = ("user_agent", "category", "boost")



class RecentConversionsTable(OfferTableBase):
	"""
	Recent Table for Conversions model.
	"""

	locker = tables.Column(verbose_name="Locker")


	class Meta(TableBase.Meta):
		model = Conversion
		orderable = False
		attrs = {"class": "ui table"}
		fields = ("locker", "ip_address", "payout", "datetime")
		empty_text = "Your most recent conversions will appear here."


	def render_datetime(self, value):
		"""
		Returns humanized since datetime value.
		"""
		return timesince(value) + " ago"


	def render_payout(self, value, record):
		"""
		Returns payout with a 'tag' link to the Offer page.
		"""
		value = super(__class__, self).render_payout(value)

		if not record.offer_id:
			return value
			
		return mark_safe("%s %s" % (
			value,
			"<a href=\"%s\"><i class=\"tag icon\"></i></a>" % (
				reverse("offers:detail", args=(record.offer_id,))
			)
		))