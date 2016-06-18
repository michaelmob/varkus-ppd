from django.contrib import admin
from .models import Conversion, Token


@admin.register(Conversion)
class Admin_Conversion(admin.ModelAdmin):
	def get_queryset(self, request):
		return super(__class__, self).get_queryset(request) \
			.prefetch_related("user", "locker").defer("offer")

	list_display = ("offer_name", "user", "locker", "sender_ip_address", "user_ip_address", "deposit", "payout", "datetime")
	search_fields = ("user_ip_address", "locker")


@admin.register(Token)
class Admin_Token(admin.ModelAdmin):
	def get_queryset(self, request):
		return super(__class__, self).get_queryset(request) \
			.prefetch_related("user", "locker")

	list_display = ("unique", "locker", "ip_address", "user_agent", "datetime", "conversion")
	search_fields = ("unique", "locker", "ip_address", "user_agent")
	filter_horizontal = ("offers",)
