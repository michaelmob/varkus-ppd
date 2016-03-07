from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.cp.templatetags.currency import currency
from apps.user.models import (Profile, Party, Earnings, Referral_Earnings)
from apps.billing.models import Billing

admin.site.unregister(User)


@admin.register(Party)
class Admin_Party(admin.ModelAdmin):
	list_display = (
		"name", "cut_amount", "referral_cut_amount"
	)


class Inline_Profile(admin.StackedInline):
	model = Profile
	fk_name = "user"
	max_num = 1

	filter_horizontal = ("offer_priority", "offer_block")


class Inline_Billing(admin.StackedInline):
	model = Billing
	fk_name = "user"
	max_num = 1


class Inline_Earnings(admin.StackedInline):
	model = Earnings
	fk_name = "obj"
	max_num = 1


class Inline_Referral_Earnings(admin.StackedInline):
	model = Referral_Earnings
	fk_name = "obj"
	max_num = 1


@admin.register(User)
class Admin_User(UserAdmin):

	def conversions(s, i): return i.earnings.conversions

	def earnings_today(s, i): return currency(i.earnings.today)

	def earnings_month(s, i): return currency(i.earnings.month)

	def earnings_total(s, i): return currency(i.earnings.total)

	inlines = [
		Inline_Profile,
		Inline_Billing,
		Inline_Earnings,
		Inline_Referral_Earnings
	]

	list_display = (
		"id", "username", "email", "last_login", "conversions",
		"earnings_today", "earnings_month", "earnings_total"
	)

	# Allow ordering
	conversions.admin_order_field = "earnings__conversions"
	earnings_today.admin_order_field = "earnings__today"
	earnings_month.admin_order_field = "earnings__month"
	earnings_total.admin_order_field = "earnings__total"
