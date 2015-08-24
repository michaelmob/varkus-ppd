from datetime import date, timedelta
from calendar import monthrange

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

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

a = {
	"blank": True,
	"null": True,
	"default": "",
}

PAYMENT_FREQUENCY = (
	("10", "Net 10"),
	("15", "Net 15"),
	("30", "Net 30"),
	("60", "Net 60")
)

class Billing(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	method = models.CharField(max_length=15, default="none", choices=PAYMENT_CHOICES)
	frequency = models.CharField(max_length=15, default="15", choices=PAYMENT_FREQUENCY)

	pending_earnings = models.DecimalField(
		max_digits=50, decimal_places=2, default=0.00)

	paid_earnings = models.DecimalField(
		max_digits=50, decimal_places=2, default=0.00)

	# Paypal
	paypal_email = models.EmailField(max_length=100, **a)

	# Check
	check_pay_to 	= models.CharField(max_length=100, **a)
	check_address 	= models.TextField(max_length=300, **a)

	# Wire
	wire_beneficiary_name	= models.CharField(max_length=100, **a)
	wire_account_number 	= models.CharField(max_length=100, **a)
	wire_bank_name			= models.CharField(max_length=100, **a)
	wire_routing_aba_swift 	= models.CharField(max_length=100, **a)
	wire_bank_address		= models.TextField(max_length=300, **a)
	wire_additional 		= models.TextField(max_length=300, **a)

	# Direct Deposit / ACH
	direct_account_holder 	= models.CharField(max_length=100, **a)
	direct_account_number 	= models.CharField(max_length=100, **a)
	direct_routing_number 	= models.CharField(max_length=100, **a)
	direct_bank_name 		= models.CharField(max_length=100, **a)
	direct_additional 		= models.TextField(max_length=300, **a)

	additional 				= models.TextField(max_length=300, **a)


class Invoice(models.Model):
	user 				= models.ForeignKey(User)

	creation_date 		= models.DateField()
	due_date 			= models.DateField()

	billing_start_date 	= models.DateField()
	billing_end_date 	= models.DateField()

	total_amount 		= models.DecimalField(max_digits=10, decimal_places=2)
	referral_amount		= models.DecimalField(max_digits=10, decimal_places=2)

	paid 				= models.BooleanField(default=False)
	error 				= models.BooleanField(default=False)

	details 			= models.TextField(max_length=1000, default="", blank=True, null=True)
	file 				= models.FileField(upload_to="billing/%b-%Y/", default=None, blank=True, null=True)

	def create(user, year, month, due_in_days, total_amount, referral_amount):
		end_date = date(year, month, monthrange(year, month)[1])
		return Invoice.objects.create(
			user 				= user,
			creation_date 		= date(year, month, 1),
			due_date			= end_date + timedelta(days=due_in_days),

			billing_start_date 	= date(year, month, 1),
			billing_end_date 	= end_date,

			total_amount		= total_amount,
			referral_amount		= referral_amount
		)

	def create_auto(user):
		minimum_payout = user.profile.party.minimum_payout

		user_earnings 		= user.earnings.month
		referral_earnings 	= user.referral_earnings.month
		pending_earnings 	= user.billing.pending_earnings
		total_earnings 		= user_earnings + referral_earnings

		# If total earnings and pending earnings don't add up to
		# the minimum payout amount, just add to the pending
		if total_earnings + pending_earnings < minimum_payout:
			user.billing.pending_earnings += total_earnings
			user.billing.save()
			return None

		today = date.today()
		due_in_days = 15

		try:
			due_in_days = int(user.billing.frequency)
		except:
			user.billing.error = True
			user.billing.save()

		return Invoice.create(
			user 			= user,
			year			= today.year,
			month			= today.month,
			due_in_days		= due_in_days,
			total_amount	= user_earnings,
			referral_amount	= referral_earnings
		)

	# INTENSE!!!
	def generate():
		users = User.objects.filter(
			Q(earnings__month__gt=0) |
			Q(referral_earnings__month__gt=0) |
			Q(billing__pending_earnings__gt=4.99)
		)

		for user in users:
			Invoice.create_auto(user)
