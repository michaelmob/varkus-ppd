from django.contrib import admin
from .models import Offer, Earnings
from django.core.urlresolvers import reverse


class Inline_Earnings(admin.StackedInline):
	model = Earnings


@admin.register(Offer)
class Admin_Offer(admin.ModelAdmin):
	inlines = [Inline_Earnings]
	list_display = (
		"name", "anchor", "category", "user_agent",
		"date", "country_count", "flag", "earnings_per_click",
		"payout", "success_rate"
	)
	search_fields = ["name", "country", "anchor"]
