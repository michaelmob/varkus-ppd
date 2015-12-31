import django_tables2 as tables

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from apps.offers.models import Offer
from apps.offers.tables import Table_Offer_Base
from apps.leads.models import Lead
from apps.cp.templatetags.currency import currency, cut_percent


class Table_Offer(Table_Offer_Base):
	name = tables.Column(accessor="name")

	class Meta:
		sortable = False
		model = Offer
		attrs = {"class": "ui table"}
		fields = ("name", "flag", "earnings_per_click", "payout")

	def create(request, objects):
		table = Table_Offer(objects)
		table.cut_amount = request.user.profile.party.cut_amount
		return table


class Table_Lead(tables.Table):
	name = tables.Column(accessor="name")
	cut_amount = 1

	class Meta:
		orderable = False
		model = Lead
		empty_text = "No leads exist."
		attrs = {"class": "ui sortable table"}
		fields = ("name", "category", "flag",
			"user_agent", "earnings_per_click", "payout")

	def create(request, objects):
		table = Table_Offer(objects)
		tables.RequestConfig(request, paginate={"per_page": 30}).configure(table)
		table.cut_amount = request.user.profile.party.cut_amount
		return table

	def render_name(self, value, record):
		return mark_safe("<a href='%s'>%s</a>" % (reverse("offers-manage", args=(record.id,)), value))

	def render_earnings_per_click(self, value):
		return "$%s" % (currency(cut_percent(value, self.cut_amount)))

	def render_payout(self, value):
		return "$%s" % (currency(cut_percent(value, self.cut_amount)))

	def render_flag(self, value, record):
		value = value.lower()
		if value == "intl":
			value == "world icon"

		result = "<i class='%s flag' alt='%s'></i> " % (value, value.upper())

		if record.country_count > 1:
			result += "<small>%s more</small>" % (record.country_count - 1)

		return mark_safe(result)
