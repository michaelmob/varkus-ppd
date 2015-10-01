import django_tables2 as tables

from django.core.urlresolvers import reverse
from django.utils.formats import date_format
from django.utils.safestring import mark_safe

from apps.cp.templatetags.currency import currency

from .models import Invoice


class Table_Invoice(tables.Table):
	billing_period = tables.Column(accessor="billing_end_date", verbose_name="Billing Period")

	class Meta:
		model = Invoice
		empty_text = "There are no invoices associated with yours account."
		attrs = {"class": "ui sortable table"}
		fields = ("creation_date", "billing_period", "total_amount", "due_date",)

	def create(request):
		table = __class__(Invoice.objects.filter(user=request.user).order_by("-creation_date"))
		tables.RequestConfig(request, paginate={"per_page": 30}).configure(table)
		return table

	def render_total_amount(self, value):
		return "$%s" % currency(value)

	def render_billing_period(self, value, record):
		return "%s - %s" % (
			date_format(record.billing_start_date, "SHORT_DATE_FORMAT"),
			date_format(record.billing_end_date, "SHORT_DATE_FORMAT"))

	def render_due_date(self, value, record):
		result = date_format(record.due_date, "SHORT_DATE_FORMAT")

		if record.paid:
			result += " <span class='ui basic label green'>Paid</span>"

		return mark_safe(result)