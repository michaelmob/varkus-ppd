from django.contrib import admin
from .models import Lead, Token


@admin.register(Lead)
class Admin_Lead(admin.ModelAdmin):
	list_display = ("offer_name", "user", "token", "sender_ip_address", "user_ip_address", "deposit", "payout", "date_time")
	search_fields = ["user_ip_address"]


@admin.register(Token)
class Admin_Token(admin.ModelAdmin):
	list_display = ("unique", "ip_address", "user_agent", "lead", "paid", "staff")
	search_fields = ["unique", "ip_address", "user_agent"]
