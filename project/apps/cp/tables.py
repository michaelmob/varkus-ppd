import django_tables2 as tables

from django.utils.timesince import timesince
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from apps.conversions.models import Conversion
from apps.offers.models import Offer
from apps.site.tables import Table_Base
from apps.offers.tables import Table_Offer_Base


class Table_Offer(Table_Offer_Base):
	name = tables.Column(accessor="name")

	class Meta(Table_Offer_Base.Meta):
		model = Offer
		orderable = False
		attrs = {"class": "ui table"}
		fields = ("name", "flag", "earnings_per_click", "payout")


class Table_Conversions(Table_Offer_Base):
	locker = tables.Column(verbose_name="Locker")

	class Meta(Table_Base.Meta):
		model = Conversion
		orderable = False
		attrs = {"class": "ui table"}
		fields = ("locker", "user_ip_address", "user_payout", "datetime")
		empty_text = "Your most recent conversions will appear here."

	def render_datetime(self, value):
		return timesince(value) + " ago"

	def render_user_payout(self, record, value):
		if not record.offer_id:
			return
			
		return mark_safe("%s %s" % (
			super(__class__, self).render_user_payout(value),
			"<a href=\"%s\"><i class=\"tag icon\"></i></a>" % (
				reverse("offers-manage", args=(record.offer_id,))
			)
		))