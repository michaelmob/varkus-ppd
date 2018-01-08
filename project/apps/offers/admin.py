from django.contrib import admin
from .models import Offer, Earnings
from django.urls import reverse



class EarningsInline(admin.StackedInline):
	"""
	Inline field for Earnings for Offer Admin page.
	"""
	model = Earnings



@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
	"""
	Model Admin for Offers.
	"""
	show_full_result_count = False
	inlines = (EarningsInline,)
	search_fields = ("name", "country", "anchor")
	list_display = (
		"name", "anchor", "category", "user_agent", "date", "country_count",
		"country", "earnings_per_click", "payout", "success_rate"
	)