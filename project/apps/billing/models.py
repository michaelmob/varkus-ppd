from datetime import date, timedelta
from calendar import monthrange
from decimal import Decimal

from django.db import models
from django.db.models import Q, Sum
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

from utils.constants import CURRENCY, DEFAULT_BLANK_NULL, BLANK_NULL


PAYMENT_CHOICES = (
	("NONE", "None"),
	("PAYPAL", "Paypal"),
	("CHECK", "Check"),
	("WIRE", "Wire"),
	("DIRECT", "Direct Deposit/ACH"),
)

PAYMENT_ICONS = {
	"NONE": "payment",
	"PAYPAL": "paypal",
	"CHECK": "write",
	"WIRE": "payment",
	"DIRECT": "forward"
}

PAYMENT_CHOICES_DICT = dict(PAYMENT_CHOICES)
PAYMENT_CHOICE_LIST = list(PAYMENT_CHOICES_DICT.keys())
PAYMENT_CHOICE_LIST.remove("NONE")


class Billing(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	choice = models.CharField(max_length=15, default="NONE",
		choices=PAYMENT_CHOICES)
	pending_earnings = models.DecimalField(**CURRENCY)
	paid_earnings = models.DecimalField(**CURRENCY)
	data = JSONField(default=dict)


class Invoice(models.Model):
	user 				= models.ForeignKey(User)

	creation_date 		= models.DateField(verbose_name="Creation Date")
	due_date 			= models.DateField(verbose_name="Due Date")

	billing_start_date 	= models.DateField()
	billing_end_date 	= models.DateField()

	total_amount 		= models.DecimalField(verbose_name="Total Amount", **CURRENCY)
	referral_amount		= models.DecimalField(**CURRENCY)

	paid 				= models.BooleanField(default=False)
	error 				= models.BooleanField(default=False)

	details 			= models.TextField(max_length=1000, default="", **BLANK_NULL)
	file 				= models.FileField(upload_to="billing/%b-%Y/", **DEFAULT_BLANK_NULL)


	def create(user):
		# I made $20 in January, so I make an invoice on February 1st to payout
		# the $20 on February 15th

		# Dates
		due 	= date.today().replace(day=15)
		start 	= (due.replace(day=1) - timedelta(days=1)).replace(day=1)
		end 	= start.replace(day=monthrange(start.year, start.month)[1])

		# No duplicate invoices allowed
		if Invoice.objects.filter(user=user, due_date=due).exists():
			return

		# Sum all of user's conversions up to get user_earnings
		user_earnings = (user.earnings.get_conversions_u((start, end))
			.aggregate(sum=Sum("user_payout"))["sum"] or 0)

		c = user.earnings.get_conversions_u((start, end))[0]

		# Sum all of user's referral earnings up
		if user.profile.referrer:
			referral_earnings = (user.profile.referrer.earnings.get_conversions_u((start, end))
				.aggregate(sum=Sum("referral_payout"))["sum"] or 0)
		else:
			referral_earnings = 0

		# Sum up user's earnings, referral's earnings, and pending earnings
		total_earnings = user_earnings + referral_earnings

		# Add to pending_earnings
		user.billing.pending_earnings += Decimal(total_earnings)
		user.billing.save()

		# Pending earnings must be greater than minimum payout for an invoice
		if user.billing.pending_earnings < Decimal(user.profile.party.minimum_payout):
			return

		return Invoice.objects.create(
			user 				= user,
			creation_date 		= date.today(),
			due_date 			= due,

			billing_start_date 	= start,
			billing_end_date 	= end,

			total_amount		= total_earnings,
			referral_amount		= referral_earnings
		)


	def create_all():
		users = User.objects.filter(
			Q(earnings__month__gt=0) | Q(referral_earnings__month__gt=0) |
			Q(billing__pending_earnings__gte=5))

		count = 0

		for user in users:
			Invoice.create(user)
			count += 1

		return count