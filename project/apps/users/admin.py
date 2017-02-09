from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.admin import InlineInline
from core.templatetags.currency import currency
from users.models import (Profile, Party, Earnings, ReferralEarnings)
from billing.models import Billing


admin.site.unregister(User)



@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
	"""
	Admin for Party model.
	"""
	show_full_result_count = False
	list_display = ("name", "cut_amount", "referral_cut_amount")



class InlineMixin():
	"""
	Base for inline fieldsets.
	"""
	max_num = 1
	can_delete = False



class ProfileInline(InlineMixin, admin.StackedInline):
	"""
	Inline fieldset for Profile foreignkey.
	"""
	model = Profile
	fk_name = "user"
	raw_id_fields = ("referrer",)
	exclude = ("offer_priority", "offer_block")



class BillingInline(InlineMixin, admin.StackedInline):
	"""
	Inline fieldset for Profile foreignkey.
	"""
	model = Billing
	fk_name = "user"



class EarningsInline(InlineMixin, InlineInline):
	"""
	Inline fieldset for Earnings foreignkey.
	"""
	model = Earnings
	fk_name = "parent"



class ReferralEarningsInline(InlineMixin, InlineInline):
	"""
	Inline fieldset for Referral Earnings foreignkey.
	"""
	model = ReferralEarnings
	fk_name = "parent"



@admin.register(User)
class UserAdmin(UserAdmin):
	"""
	Model Admin for Users.
	"""
	show_full_result_count = False

	inlines = [
		EarningsInline, ReferralEarningsInline, ProfileInline, BillingInline
	]

	list_display = (
		"username", "email", "last_login", "conversions",
		"earnings_today", "earnings_month", "earnings_total"
	)


	def conversions(self, instance):
		"""
		Returns user's conversion count.
		"""
		return instance.earnings.conversions


	def earnings_today(self, instance):
		"""
		Returns user's earnings for today.
		"""
		return currency(instance.earnings.today)


	def earnings_month(self, instance):
		"""
		Returns user's earnings this month.
		"""
		return currency(instance.earnings.month)


	def earnings_total(self, instance):
		"""
		Returns user's total earnings.
		"""
		return currency(instance.earnings.total)


	def get_fieldsets(self, *args, **kwargs):
		"""
		Exclude 'groups' and 'permissions' from permissions area.
		They are currently unused in the project and run unneeded queries.
		"""
		fieldsets = super(__class__, self).get_fieldsets(*args, **kwargs)
		try:
			fieldsets[2][1]["fields"] = ("is_active", "is_staff", "is_superuser")
		except:
			pass
		return fieldsets


	def get_queryset(self, request):
		"""
		Chain prefetch_related onto queryset to make it more efficient.
		"""
		result = super(__class__, self).get_queryset(request)

		# On change page, do not include it because it runs another query.
		if not request.get_full_path().endswith("/change/"):
			return result.prefetch_related("earnings")

		return result


	# Must be at the bottom
	conversions.admin_order_field = "earnings__conversions"
	earnings_today.admin_order_field = "earnings__today"
	earnings_month.admin_order_field = "earnings__month"
	earnings_total.admin_order_field = "earnings__total"