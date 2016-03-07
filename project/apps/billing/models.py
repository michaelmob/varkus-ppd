from datetime import date, timedelta
from calendar import monthrange

from django.db import models
from django.db.models import Q, Sum

from django.contrib.auth.models import User

from apps.conversions.models import Conversion


PAYMENT_CHOICES = (
	("none", "None"),
	("paypal", "Paypal"),
	("check", "Check"),
	("wire", "Wire"),
	("direct", "Direct Deposit/ACH"),
)

PAYMENT_ICONS = {
	"none": "payment",
	"paypal": "paypal",
	"check": "write",
	"wire": "payment",
	"direct": "forward"
}

PAYMENT_CHOICES_DICT = dict(PAYMENT_CHOICES)
PAYMENT_CHOICES_USER_DICT = PAYMENT_CHOICES_DICT
del PAYMENT_CHOICES_USER_DICT["none"]
PAYMENT_CHOICE_LIST = PAYMENT_CHOICES_USER_DICT.keys()


# Null, Blank, and Empty Default preset
DEFAULTS = { "null": True, "blank": True, "default": "" }

class Billing(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	method = models.CharField(max_length=15, default="none", choices=PAYMENT_CHOICES)

	pending_earnings = models.DecimalField(
		max_digits=50, decimal_places=2, default=0.00)

	paid_earnings = models.DecimalField(
		max_digits=50, decimal_places=2, default=0.00)

	# Paypal
	paypal_email = models.EmailField(max_length=100, **DEFAULTS)

	# Check
	check_pay_to 	= models.CharField(max_length=100, **DEFAULTS)
	check_address 	= models.TextField(max_length=300, **DEFAULTS)

	# Wire
	wire_beneficiary_name	= models.CharField(max_length=100, **DEFAULTS)
	wire_account_number 	= models.CharField(max_length=100, **DEFAULTS)
	wire_bank_name			= models.CharField(max_length=100, **DEFAULTS)
	wire_routing_aba_swift 	= models.CharField(max_length=100, **DEFAULTS)
	wire_bank_address		= models.TextField(max_length=300, **DEFAULTS)
	wire_additional 		= models.TextField(max_length=300, **DEFAULTS)

	# Direct Deposit / ACH
	direct_account_holder 	= models.CharField(max_length=100, **DEFAULTS)
	direct_account_number 	= models.CharField(max_length=100, **DEFAULTS)
	direct_routing_number 	= models.CharField(max_length=100, **DEFAULTS)
	direct_bank_name 		= models.CharField(max_length=100, **DEFAULTS)
	direct_additional 		= models.TextField(max_length=300, **DEFAULTS)

	additional 				= models.TextField(max_length=300, **DEFAULTS)



class Invoice(models.Model):
	user 				= models.ForeignKey(User)

	creation_date 		= models.DateField(verbose_name="Creation Date")
	due_date 			= models.DateField(verbose_name="Due Date")

	billing_start_date 	= models.DateField()
	billing_end_date 	= models.DateField()

	total_amount 		= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
	referral_amount		= models.DecimalField(max_digits=10, decimal_places=2)

	paid 				= models.BooleanField(default=False)
	error 				= models.BooleanField(default=False)

	details 			= models.TextField(max_length=1000, default="", blank=True, null=True)
	file 				= models.FileField(upload_to="billing/%b-%Y/", default=None, blank=True, null=True)


	def create(user, due_date, billing_start, billing_end, total_amount, referral_amount):

		return Invoice.objects.create(
			user 				= user,
			creation_date 		= date.today(),
			due_date			= due_date,

			billing_start_date 	= billing_start,
			billing_end_date 	= billing_end,

			total_amount		= total_amount,
			referral_amount		= referral_amount)


	#I made $20 in January, so I make an invoice on February 1st to payout the $20 on February 15th
	def create_auto(user):
		# Dates
		due_date 	= date.today().replace(day=15)
		start 		= (due_date.replace(day=1) - timedelta(days=1)).replace(day=1)
		end 		= start.replace(day=monthrange(start.year, start.month)[1])

		# No duplicate invoices allowed
		if Invoice.objects.filter(user=user, due_date=due_date).exists():
			return

		# Sum all of user's conversions up to get user_earnings
		user_earnings = user.earnings.get_conversions_u((start, end)) \
			.aggregate(e=Sum("user_payout"))["e"] or 0

		# Sum all of user's referral earnings up
		if user.profile.referrer:
			referral_earnings = user.profile.referrer.earnings.get_conversions_u((start, end)) \
				.aggregate(e=Sum("referral_payout"))["e"] or 0
		else:
			referral_earnings = 0

		total_earnings = user_earnings + referral_earnings

		# Add pending earnings
		user.billing.pending_earnings += total_earnings
		user.billing.save()

		# Total and pending must be greater than minimum payout for an invoice
		if total_earnings + user.billing.pending_earnings < user.profile.party.minimum_payout:
			return

		return Invoice.create(
			user 			= user,
			due_date 		= due_date,
			billing_start 	= start,
			billing_end 	= end,
			total_amount	= total_earnings,
			referral_amount	= referral_earnings)


	def generate():
		users = User.objects.filter(
			Q(earnings__month__gt=0) | Q(referral_earnings__month__gt=0) |
			Q(billing__pending_earnings__gte=5))

		count = 0

		for user in users:
			Invoice.create_auto(user)
			count += 1

		return count