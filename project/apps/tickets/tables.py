from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from core.tables import tables, TableBase
from .models import Thread



class TicketTable(tables.Table):
	"""
	Table for Ticket model.
	"""
	subject = tables.LinkColumn("tickets:detail", text=lambda r: r.subject, args=(tables.A("id"),))
	status = tables.Column(accessor="closed")


	class Meta(TableBase.Meta):
		model = Thread
		empty_text = "You have not created a ticket."
		fields = ("subject", "datetime", "last_replier", "priority", "status")


	def render_last_replier(self, value):
		"""
		Return last replier for Ticket.
		"""
		return value.title()


	def render_status(self, value, record):
		"""
		Return HTML span element for status column.
		"""
		if record.closed:
			color, text = ("red", "Closed")
		elif record.unread:
			color, text = ("blue", "Respond")
		else:
			color, text = ("green", "Open")

		return mark_safe("<span class='ui label %s'>%s</span>" % (color, text))