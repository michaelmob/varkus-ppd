import django_tables2 as tables

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from apps.leads.models import Lead
from .models import Offer
from apps.cp.templatetags.currency import currency, cut_percent


class Table_Offer_Base(tables.Table):
	def render_name(self, value, record):
		return mark_safe("<a href='%s'>%s</a>" % (reverse("offers-manage", args=(record.id,)), value))

	def render_offer(self, value, record):
		offer = record.offer
		return mark_safe("<a href='%s'>%s</a>" % (reverse("offers-manage", args=(offer.id,)), offer.name))

	def render_earnings_per_click(self, value):
		return "$%s" % (currency(cut_percent(value, self.cut_amount)))

	def render_payout(self, value):
		return "$%s" % (currency(cut_percent(value, self.cut_amount)))

	def render_user_payout(self, value):
		return "$" + str(value)

	def render_flag(self, value, record):
		value = value.lower()

		if value == "intl":
			value = "world icon"

		result = "<i class='%s flag' alt='%s'></i> " % (value, value.upper())

		if record.country_count > 1:
			result += "<small>%s more</small>" % (record.country_count - 1)

		return mark_safe(result)

	def render_ip_address(self, value, record):
		country = record.country.lower()
		result = "<i class='%s flag' alt='%s'></i> %s" % (country, country.upper(), value)

		return mark_safe(result)

	def render_user_ip_address(self, value, record):
		return self.render_ip_address(value, record)

	def render_success_rate(self, value):
		return "%.3g%%" % value


class Table_Offer_All(Table_Offer_Base):
	name = tables.Column(accessor="name")
	cut_amount = 1

	class Meta:
		model = Lead
		attrs = {"class": "ui sortable table"}
		empty_text = "No offers matching your search exist."
		fields = ("name", "category", "flag",
			"user_agent", "earnings_per_click", "payout")

	def create(request, objects):
		table = __class__(objects)
		tables.RequestConfig(request, paginate={"per_page": 30}).configure(table)
		table.cut_amount = request.user.profile.party.cut_amount or settings.DEFAULT_CUT_AMOUNT
		return table


class Table_Offer_Leads(Table_Offer_Base):
	class Meta:
		model = Lead
		attrs = {"class": "ui sortable table"}
		empty_text = "You haven't received any leads with this offer."
		fields = ("user_ip_address", "user_payout", "date_time", "approved")

	def create(request, objects):
		table = __class__(objects)
		tables.RequestConfig(request, paginate={"per_page": 5}).configure(table)
		return table


class Table_Offer_Options(Table_Offer_Base):
	remove = tables.Column(empty_values=(), orderable=False)

	class Meta:
		model = Lead
		attrs = {"class": "ui sortable table"}
		empty_text = "There are no offers in this list."
		fields = ("name", "category", "flag")

	def create(request, objects):
		table = __class__(objects)
		tables.RequestConfig(request, paginate={"per_page": 30}).configure(table)
		return table

	def render_remove(self, record):
		return mark_safe(
			"<button data-id='%s' class='ui fluid left labeled icon remove button mini'><i class='remove icon'></i>Remove</button>" %\
				(record.pk,))
