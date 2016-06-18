from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from apps.cp.templatetags.currency import currency
from apps.conversions.models import Token, Conversion
from apps.offers.tables import Table_Offer_Base, tables
from apps.site.tables import Table_Base


class Table_Locker_Base(tables.Table):
	name = tables.Column(accessor="name", verbose_name="Name")
	earnings_conversions = tables.Column(accessor="earnings.conversions", verbose_name="Conversions")
	earnings_clicks = tables.Column(accessor="earnings.clicks", verbose_name="Clicks")
	earnings_month = tables.Column(accessor="earnings.month", verbose_name="Month")
	earnings_total = tables.Column(accessor="earnings.total", verbose_name="Total")

	class Meta(Table_Base.Meta):
		model = None
		orderable = True
		empty_text = "You have not uploaded any files."
		fields = ("name", "earnings_conversions", "earnings_clicks",
			"earnings_month", "earnings_total", "datetime")
		prefix = "locker_"

	def __init__(self, request, data=None, **kwargs):
		if not data:
			data = self.Meta.model.objects.filter(user=request.user)

		super(__class__, self).__init__(data, **kwargs)
		tables.RequestConfig(request, paginate={ 
			"per_page": settings.ITEMS_PER_PAGE_MEDIUM }).configure(self)
		self._name = self.__class__.__name__[6:].lower() + "s"

	def render_name(self, value, record):
		return mark_safe("<a href='%s'>%s</a>" % (reverse(self._name + "-manage",
			args=(record.code,)), value))

	def render_earnings_total(self, value):
		return "$%s" % currency(value)

	def render_earnings_month(self, value):
		return self.render_earnings_total(value)


class Table_Locker_Conversions(Table_Offer_Base):
	approved = tables.Column(accessor="approved", verbose_name="")
	cut_amount = 1

	class Meta(Table_Base.Meta):
		orderable = True
		model = Conversion
		empty_text = "This locker has not received any conversions."
		fields = ("offer", "user_ip_address", "user_payout", "datetime", "approved")
		prefix = "conversions-"
	
	def render_approved(self, record):
			return mark_safe("<span class=\"ui %s horizontal label\">%s</span>" % \
				("green" if record.approved else "red",
					"Approved" if record.approved else "Chargeback"))


class Table_Locker_Clicks(Table_Offer_Base):
	cut_amount = 1

	class Meta(Table_Base.Meta):
		orderable = True
		model = Token
		empty_text = "This locker has not received any clicks."
		fields = ("ip_address", "last_access")
		prefix = "clicks-"