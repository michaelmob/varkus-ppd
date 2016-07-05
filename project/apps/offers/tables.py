import django_tables2 as tables

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from apps.conversions.models import Conversion
from .models import Offer
from apps.site.tables import Table_Base, tables
from apps.cp.templatetags.currency import currency, cut_percent


class Table_Offer_Base(tables.Table):
	class Meta(Table_Base.Meta):
		pass

	def __init__(self, request, data, per_page=5, **kwargs):
		self.cut_amount = request.user.profile.party.cut_amount
		super(__class__, self).__init__(data)
		tables.RequestConfig(request,
			paginate={"per_page": per_page}).configure(self)

	def render_name(self, value, record):
		return mark_safe("<a href='%s'>%s</a>" % (reverse("offers-manage", args=(record.id,)), value))

	def render_offer(self, value, record):
		offer = record.offer
		return mark_safe("<a href='%s'>%s</a>" % (
			reverse("offers-manage", args=(offer.id,)), offer.name))

	def render_locker(self, value, record):
		locker = record.locker
		return mark_safe("<a href='%s'>%s</a>" % (locker.get_manage_url(),
			locker.get_type().title() + ": " + locker.name))

	def render_approved(self, record):
		return mark_safe("<span class=\"ui %s horizontal label\">%s</span>" % \
			("green" if record.approved else "red",
				"Approved" if record.approved else "Chargeback"))

	def render_earnings_per_click(self, value):
		return "$%s" % currency(cut_percent(value, self.cut_amount))

	def render_payout(self, value):
		return "$%s" % currency(cut_percent(value, self.cut_amount))

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
		result = "<i class='%s flag' alt='%s'></i>%s" % (country, country.upper(), value)

		return mark_safe(result)

	def render_user_ip_address(self, value, record):
		return self.render_ip_address(value, record)

	def render_success_rate(self, value):
		return "%.3g%%" % value


class Table_Offer_All(Table_Offer_Base):
	cut_amount = 1

	class Meta(Table_Offer_Base.Meta):
		model = Conversion
		empty_text = "No offers matching your search exist."
		fields = ("name", "category", "flag",
			"user_agent", "earnings_per_click", "payout")


class Table_Offer_Conversions(Table_Offer_Base):
	approved = tables.Column(accessor="approved", verbose_name="Status")

	class Meta(Table_Offer_Base.Meta):
		model = Conversion
		empty_text = "You haven't received any conversions with this offer."
		fields = ("user_ip_address", "user_payout", "datetime", "approved")


class Table_Offer_Options(Table_Offer_Base):
	remove = tables.Column(empty_values=(), orderable=False)

	class Meta(Table_Offer_Base.Meta):
		model = Conversion
		empty_text = "There are no offers in this list."
		fields = ("name", "category", "flag")

	def render_remove(self, record):
		return mark_safe(
			"<a data-id='%s' class='ui fluid left labeled icon remove button mini'><i class='remove icon'></i>Remove</a>" %\
				(record.pk,))
