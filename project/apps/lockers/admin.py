from django.contrib.admin import ModelAdmin
from core.templatetags.currency import currency



class ModelAdminMixin(ModelAdmin):
	"""
	Mixin for model admins.
	"""
	change_form_template = "admin/lockers/locker/change_form.html"
	show_full_result_count = False
	search_fields = ("name", "description")
	list_display = (
		"name", "user", "conversions", "earnings_today",
		"earnings_month", "earnings_total", "datetime"
	)


	def conversions(sender, instance):
		"""
		Returns conversion count from earnings object.
		"""
		return instance.earnings.conversions


	def earnings_today(sender, instance):
		"""
		Returns today's earnings from earnings object.
		"""
		return currency(instance.earnings.today)


	def earnings_month(sender, instance):
		"""
		Returns month's earnings from earnings object.
		"""
		return currency(instance.earnings.month)


	def earnings_total(sender, instance):
		"""
		Returns total earnings from earnings object.
		"""
		return currency(instance.earnings.total)


	# Allow ordering; must be below functions
	conversions.admin_order_field = "earnings__conversions"
	earnings_today.admin_order_field = "earnings__today"
	earnings_month.admin_order_field = "earnings__month"
	earnings_total.admin_order_field = "earnings__total"