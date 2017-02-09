from django.contrib import admin
from .models import Conversion, Token, Boost



@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
	"""
	Model Admin for Conversions.
	"""
	list_display = ("offer_name", "user", "locker", "accessor_ip_address", "ip_address", "deposit", "payout", "datetime")
	search_fields = ("ip_address", "locker")
	show_full_result_count = False
	raw_id_fields = ("user",)


	def get_queryset(self, request):
		"""
		Chain prefetch_related onto queryset to make it more efficient.
		"""
		return (
			super(__class__, self)
				.get_queryset(request)
				.prefetch_related("user", "locker")
				.defer("offer")
			)



@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
	"""
	Model Admin for Tokens.
	"""
	list_display = ("unique", "locker", "ip_address", "user_agent", "datetime", "conversion")
	search_fields = ("unique", "locker", "ip_address", "user_agent")
	filter_horizontal = ("offers",)
	show_full_result_count = False
	raw_id_fields = ("user",)


	def get_queryset(self, request):
		"""
		Chain prefetch_related onto queryset to make it more efficient.
		"""
		return (
			super(__class__, self)
				.get_queryset(request)
				.prefetch_related("user", "locker")
		)



@admin.register(Boost)
class BoostAdmin(admin.ModelAdmin):
	"""
	Model Admin for Tokens.
	"""
	list_display = ("user", "offer", "count")
	show_full_result_count = False
	raw_id_fields = ("user", "offer")


	def get_queryset(self, request):
		"""
		Chain prefetch_related onto queryset to make it more efficient.
		"""
		return (
			super(__class__, self)
				.get_queryset(request)
				.prefetch_related("user", "offer")
		)