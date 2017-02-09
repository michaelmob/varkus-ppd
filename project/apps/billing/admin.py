from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	"""
	Admin for Invoice model.
	"""
	show_full_result_count = False
	list_display = ("user", "total_amount", "referral_amount", "creation_date", "due_date", "paid")
	search_fields = ("user",)
	raw_id_fields = ("user",)