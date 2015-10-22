import django_tables2 as tables

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from apps.leads.models import Lead
from apps.cp.templatetags.currency import currency, cut_percent


class Table_Locker_Lead(tables.Table):
	cut_amount = 1

	class Meta:
		orderable = True
		model = Lead
		empty_text = "This locker has not received any leads."
		attrs = {"class": "ui sortable table"}
		fields = ("offer", "user_ip_address", "user_payout", "date_time", "approved")

	def create(request, objects):
		table = __class__(objects)
		tables.RequestConfig(request, paginate={"per_page": 15}).configure(table)
		return table

	def render_offer(self, value, record):
		try:
			url = reverse("offers-manage", args=(record.offer.id,))
		except:
			url = "#"

		value = record.offer_name
		return mark_safe("<a href='%s'>%s</a>" % (url, value[:20] + (value[20:] and '..')))

	def render_user_payout(self, value):
		return "$" + str(value)

	def render_user_ip_address(self, value, record):
		result = "<i class='%s flag' alt='%s'></i> %s" % \
			(record.country.lower(), value.upper(), value)

		return mark_safe(result)

	def render_approved(self, value):
		if value == True:
			result = "<i class='checkmark icon'></i> Yes"
		else:
			result = "<i class='remove icon'></i> No"

		return mark_safe(result)

	def render_date_time(self, value):
		return value.strftime("%m/%d/%Y %l:%M%P")
