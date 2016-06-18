from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from apps.site.tables import tables, Table_Base
from .models import Thread

class Table_Tickets(tables.Table):
	status = tables.Column(empty_values=(), orderable=False)
	last_replier = tables.Column(empty_values=(), orderable=False)

	class Meta(Table_Base.Meta):
		model = Thread
		attrs = {"class": "ui sortable table"}
		empty_text = "You have not created a ticket."
		fields = ("subject", "datetime", "last_replier", "priority", "status")

	def __init__(self, request, data=None, per_page=30, **kwargs):
		if not data:
			data = Thread.objects.filter(user=request.user)

		super(__class__, self).__init__(data)
		tables.RequestConfig(request,
			paginate={"per_page": per_page}).configure(self)

	def render_subject(self, value, record):
		return mark_safe("<a href='%s'>%s</a>" % (reverse("tickets-manage", args=(record.id,)), value))

	def render_last_replier(self, value, record):
		return ""

	def render_status(self, value, record):
		if record.closed:
			return mark_safe("<span class='ui label red'>Closed</span>")
		
		return mark_safe("<span class='ui label green'>Open</span>")