from decimal import Decimal
from datetime import date, timedelta
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from . import utils



class InvoiceManager(models.Manager):
	"""
	Manager for Invoice model.
	"""
	def create_invoice(self, user, check_for_duplicates=True):
		"""
		Create invoice for a user.
		"""
		# Dates
		today = date.today()
		period_range = utils.month_range(today.replace(day=1) - timedelta(days=1))
		due_on = utils.net_days(period_range[0], user.billing.frequency)

		# Check for duplicate invoices
		if check_for_duplicates:
			if self.filter(user=user, period_start_date=period_range[0]).exists():
				return

		# Amounts
		user_earnings = user.billing.get_earnings_sum(period_range)
		referral_earnings = user.billing.get_referral_earnings_sum(period_range)
		total_earnings = user_earnings + referral_earnings

		# Add pending earnings
		user.billing.pending_earnings += Decimal(total_earnings)
		user.billing.save()

		# Pending earnings must be greater than minimum payout for an invoice
		if user.billing.pending_earnings < Decimal(user.profile.party.minimum_payout):
			return

		# Create invoice
		return self.create(
			user 				= user,
			creation_date 		= today,
			due_date 			= due_on,

			period_start_date 	= period_range[0],
			period_end_date 	= period_range[1] - timedelta(days=1),

			total_amount		= total_earnings,
			referral_amount		= referral_earnings
		)


	def create_all_invoices(self, check_for_duplicates=True):
		"""
		Create invoices for all users.
		"""
		count = 0
		users = User.objects.filter(
			Q(earnings__month__gt=0) | Q(referralearnings__month__gt=0) |
			Q(billing__pending_earnings__gte=5)
		)

		for user in users:
			if self.create_invoice(user, check_for_duplicates):
				count += 1

		return count