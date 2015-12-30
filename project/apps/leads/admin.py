from django.contrib import admin
from .models import Lead, Token


@admin.register(Lead)
class Admin_Lead(admin.ModelAdmin):
	list_display = ("offer_name", "user", "token", "locker", "sender_ip_address", "user_ip_address", "deposit", "payout", "date_time")
	search_fields = ("user_ip_address", "locker")


@admin.register(Token)
class Admin_Token(admin.ModelAdmin):
	list_display = ("unique", "locker", "ip_address", "user_agent", "date_time", "lead", "paid", "staff")
	search_fields = ("unique", "locker", "ip_address", "user_agent")
	filter_horizontal = ("offers",)