import django_tables2 as tables

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import File
from apps.cp.templatetags.currency import currency


class Table_File(tables.Table):
	name = tables.Column(accessor="name", verbose_name="Name")
	earnings_leads = tables.Column(accessor="earnings.leads", verbose_name="Leads")
	earnings_clicks = tables.Column(accessor="earnings.clicks", verbose_name="Clicks")
	earnings_month = tables.Column(accessor="earnings.month", verbose_name="Month")
	earnings_total = tables.Column(accessor="earnings.total", verbose_name="Total")

	class Meta:
		model = File
		orderable = True
		empty_text = "You have not uploaded any files."
		attrs = {"class": "ui sortable table"}
		fields = ("name", "earnings_leads", "earnings_clicks", "earnings_month", "earnings_total", "date_time")

	def create(request):
		table = Table_File(File.objects.filter(user=request.user))
		tables.RequestConfig(request, paginate={"per_page": 15}).configure(table)
		return table

	def render_name(self, value, record):
		return mark_safe("<a href='%s'>%s</a>" % (reverse("files-manage", args=(record.code,)), value))

	def render_earnings_total(self, value):
		return "$%s" % currency(value)

	def render_earnings_month(self, value):
		return self.render_earnings_total(value)