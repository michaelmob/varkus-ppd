import django_tables2 as tables

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.formats import date_format
from django.utils.safestring import mark_safe

from apps.cp.templatetags.currency import currency

from .models import Invoice


class Table_Invoice(tables.Table):
	billing_period = tables.Column(accessor="billing_end_date", verbose_name="Billing Period")
	referral_amount = tables.Column(accessor="referral_amount", verbose_name="Referrals")
	paid = tables.Column(accessor="paid", verbose_name="Status")
	details = tables.Column(accessor="details", verbose_name="Notes")

	class Meta:
		model = Invoice
		empty_text = "There are no invoices associated with your account."
		attrs = {"class": "ui sortable table"}
		fields = ("creation_date", "billing_period", "total_amount", "referral_amount", "paid", "due_date", "details")

	def create(request):
		table = __class__(Invoice.objects.filter(user=request.user).order_by("-creation_date"))
		tables.RequestConfig(request, paginate={"per_page": settings.ITEMS_PER_PAGE}).configure(table)
		return table

	def render_total_amount(self, value):
		return "$%s" % currency(value)

	def render_referral_amount(self, value):
		return "$%s" % currency(value)

	def render_billing_period(self, value, record):
		return "%s - %s" % (
			date_format(record.billing_start_date, "SHORT_DATE_FORMAT"),
			date_format(record.billing_end_date, "SHORT_DATE_FORMAT"))

	def render_due_date(self, value, record):
		return mark_safe(date_format(record.due_date, "SHORT_DATE_FORMAT"))

	def render_paid(self, record):
		if record.error:
			return mark_safe("<span class='ui label red'>Error</span>")
		
		if record.paid:
			return mark_safe("<span class='ui label green'>Paid</span>")

		return mark_safe("<span class='ui label orange'>Pending</span>")

	def render_details(self, value):
		if not value:
			return
			
		return mark_safe("<button data-title='Notes' data-content='%s' class='ui basic icon details button'>" % (value,) +
			"<i class='file text outline icon'></i></button>")