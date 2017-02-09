from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from billing.tables import InvoiceTable
from tickets.tables import TicketTable
from core.tables import tables, TableBase, CurrencyColumn
from axes.models import AccessLog
from billing.models import Invoice
from tickets.models import Thread



class InvoiceStaffTable(InvoiceTable):
	"""
	Invoice table for Staff users.
	"""
	id = tables.LinkColumn("staff:invoice-detail", text=lambda r: "Invoice #%s" % r.id, args=(tables.A("id"),))
	user = tables.LinkColumn("staff:user-detail", text=lambda r: r.user.username, args=(tables.A("user_id"),))

	class Meta(InvoiceTable.Meta):
		model = Invoice
		fields = ("id", "user")
		empty_text = "There are no invoices."



class TicketStaffTable(TicketTable):
	"""
	User table for Staff users.
	"""
	user = tables.LinkColumn("staff:user-detail", text=lambda r: r.user.username, args=(tables.A("user_id"),))


	class Meta(TableBase.Meta):
		model = Thread
		fields = ("subject", "user",)
		empty_text = "There are no tickets."


	def render_status(self, value, record):
		"""
		Return HTML span element for status column.
		"""
		if record.closed:
			color, text = ("red", "Closed")
		elif record.staff_unread:
			color, text = ("blue", "Respond")
		else:
			color, text = ("green", "Open")

		return mark_safe("<span class='ui label %s'>%s</span>" % (color, text))



class UserStaffTable(TableBase):
	"""
	User table for Staff users.
	"""
	username = tables.LinkColumn("staff:user-detail", text=lambda r: r.username, args=(tables.A("id"),))
	clicks = CurrencyColumn(accessor="earnings.clicks", verbose_name="Clicks")
	conversions = CurrencyColumn(accessor="earnings.conversions", verbose_name="Conversions")
	today = CurrencyColumn(accessor="earnings.today", verbose_name="Today")
	month = CurrencyColumn(accessor="earnings.month", verbose_name="Month")
	total = CurrencyColumn(accessor="earnings.total", verbose_name="Total")


	class Meta(TableBase.Meta):
		model = User
		fields = ("username", "email", "last_login")
		empty_text = "There are no users."


	def render_clicks(self, value, record):
		"""
		Render total clicks.
		"""
		return record.earnings.clicks


	def render_conversions(self, value, record):
		"""
		Render total conversions.
		"""
		return record.earnings.conversions



class AccessLogStaffTable(TableBase):
	"""
	User table for Access logs.
	"""

	class Meta(TableBase.Meta):
		model = AccessLog
		fields = ("ip_address", "attempt_time")
		empty_text = "This user has not logged in."


	def render_ip_address(self, value):
		"""
		Allow look-up by IP Address into the admin panel.
		"""
		return mark_safe(
			(
				"<a href='/admin/axes/accesslog/?ip_address={0}'>"
				"{0} <i class='shield icon'></i></a>"
			).format(value)
		)