from django.utils.html import format_html
from django.utils.safestring import mark_safe
from core.tables import tables, TableBase, CurrencyColumn
from .models import Invoice



class InvoiceTable(TableBase):
	"""
	Table to display a User's invoices.
	"""
	billing_period = tables.Column(accessor="period_end_date", verbose_name="Billing Period")
	total_amount = CurrencyColumn(verbose_name="Total")
	referral_amount = CurrencyColumn(verbose_name="Referral")
	paid = tables.Column(verbose_name="Status")
	due_date = tables.DateColumn()
	details = tables.Column(verbose_name="Notes")


	class Meta(TableBase.Meta):
		model = Invoice
		empty_text = "There are no invoices associated with your account."
		fields = ("billing_period",)


	def render_billing_period(self, value, record):
		"""
		Returns invoice's billing period.
		"""
		return "%s - %s" % (
			self.date(record.period_start_date),
			self.date(record.period_end_date)
		)
		

	def render_paid(self, record):
		"""
		Returns status of invoice.
		"""
		if record.error:
			color, text = ("red", "Error")

		elif record.paid:
			color, text = ("green", "Paid")

		else:
			color, text = ("orange", "Pending")

		return mark_safe("<span class='ui label %s'>%s</span>" % (color, text))


	def render_details(self, value):
		"""
		Return the invoice's notes and details.
		"""
		if not value:
			return
			
		return format_html(
			(
				"<button data-title='Notes' data-content='{}' class='ui basic icon details button'>"
				"<i class='file text outline icon'></i></button>"
			),
			value
		)