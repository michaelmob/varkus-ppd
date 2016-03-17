from django.contrib import admin
from .models import Conversion, Token


@admin.register(Conversion)
class Admin_Conversion(admin.ModelAdmin):
	list_display = ("offer", "user", "token", "locker", "sender_ip_address", "user_ip_address", "deposit", "payout", "date_time")
	search_fields = ("user_ip_address", "locker")


@admin.register(Token)
class Admin_Token(admin.ModelAdmin):
	list_display = ("unique", "locker", "ip_address", "user_agent", "date_time", "conversion", "paid", "staff")
	search_fields = ("unique", "locker", "ip_address", "user_agent")
	filter_horizontal = ("offers",)
