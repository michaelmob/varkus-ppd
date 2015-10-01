import django_tables2 as tables

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import Thread


class Table_Ticket(tables.Table):
	#earnings_leads = tables.Column(accessor="earnings.leads", verbose_name="Leads")

	class Meta:
		model = Thread
		orderable = True
		empty_text = "You have not created any tickets."
		attrs = {"class": "ui sortable table"}
		fields = ("subject", "date_time", "last_reply_user", "closed")

	def create(request):
		table = Table_Ticket(Thread.objects.filter(user=request.user))
		tables.RequestConfig(request, paginate={"per_page": 15}).configure(table)
		return table

	def render_subject(self, value, record):
		return mark_safe("<a href='%s'>%s</a>" % (reverse("tickets-thread", args=(record.id,)), value))

	def render_last_reply_user(self, value):
		return str(value).capitalize()

	def render_closed(self, value, record):
		if value: # == closed
			html = "<span class='ui basic label red'>Closed</span>"
		else:
			if record.is_unread():
				html = "<span class='ui basic label blue'>Unread</span>"
			else:
				html = "<span class='ui basic label green'>Open</span>"

		return mark_safe(html)