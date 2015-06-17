from django.contrib import admin
from .lists.models import List, Earnings as List_Earnings
from .files.models import File, Earnings as File_Earnings
from apps.cp.templatetags.currency import currency


# Files
class Inline_File_Earnings(admin.StackedInline):
	model = File_Earnings


@admin.register(File)
class Admin_File(admin.ModelAdmin):

	def leads(s, i): return i.earnings.leads
	def earnings_today(s, i): return currency(i.earnings.today)
	def earnings_month(s, i): return currency(i.earnings.month)
	def earnings_total(s, i): return currency(i.earnings.total)

	inlines = [Inline_File_Earnings]
	list_display = (
		"name", "file_size", "user", "leads", "earnings_today",
		"earnings_month", "earnings_total", "date_time"
	)
	search_fields = ["name", "description"]

	# Allow ordering
	leads.admin_order_field = "earnings__leads"
	earnings_today.admin_order_field = "earnings__today"
	earnings_month.admin_order_field = "earnings__month"
	earnings_total.admin_order_field = "earnings__total"

# Lists
class Inline_List_Earnings(admin.StackedInline):
	model = List_Earnings


@admin.register(List)
class Admin_List(admin.ModelAdmin):
	inlines = [Inline_List_Earnings]
	list_display = ("name",)
	search_fields = ["name"]
