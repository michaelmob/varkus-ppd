from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class Admin_Invoice(admin.ModelAdmin):
	list_display = ("user", "total_amount", "referral_amount", "creation_date", "due_date", "paid")
	search_fields = ["user"]
