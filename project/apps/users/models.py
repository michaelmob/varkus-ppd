from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from offers.models import Offer
from core.models import EarningsBase


PERCENTAGE = {
	"max_digits": 5, "decimal_places": 2,
	"validators": [MinValueValidator(0), MaxValueValidator(1)]
}


class Party(models.Model):
	"""
	Model for Party table.
	"""
	name = models.CharField(max_length=50)

	minimum_payout = models.DecimalField(
		max_digits=6, decimal_places=2, default="10.00"
	)

	cut_amount = models.DecimalField(
		default="0.30", help_text=(
			"This percentage is taken off of the users payout -- The developers cut"
		), **PERCENTAGE
	)

	referral_cut_amount = models.DecimalField(
		default="0.10", help_text=(
			"This and cut_amount should not sum up to be more than 100% (or 1)"
		), **PERCENTAGE
	)


	class Meta:
		verbose_name_plural = "Parties"


	def __str__(self):
		"""
		String representative.
		"""
		return self.name


	def get_or_create_default():
		"""
		Gets or creates default party.
		"""
		kwargs = {
			"id": settings.DEFAULT_PARTY_ID,
			"defaults": {
				"name": settings.DEFAULT_PARTY_NAME,
				"cut_amount": settings.DEFAULT_CUT_AMOUNT,
				"referral_cut_amount": settings.DEFAULT_REFERRAL_CUT_AMOUNT
			}
		}
		return Party.objects.get_or_create(**kwargs)[0]



class Profile(models.Model):
	"""
	Model for User's profile table.
	"""
	user 			= models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	party 			= models.ForeignKey(Party, related_name="party_id", blank=True, null=True, default=None, on_delete=models.SET_NULL)
	referrer 		= models.ForeignKey(User, related_name="referrer_id", blank=True, null=True, default=None, on_delete=models.SET_NULL)

	phone_number	= models.CharField(max_length=100, blank=True, null=True)
	address			= models.TextField(max_length=200, blank=True, null=True)
	city			= models.CharField(max_length=100, blank=True, null=True)
	state			= models.CharField(max_length=100, blank=True, null=True)
	country			= CountryField(blank=True, null=True)
	postal_code		= models.CharField(max_length=20, blank=True, null=True)

	company 		= models.CharField(max_length=100, blank=True, null=True)
	website			= models.URLField(max_length=100, blank=True, null=True)
	birthdate		= models.DateField(blank=True, null=True)


	offer_priority	= models.ManyToManyField(Offer, related_name="offer_priority", blank=True)
	offer_block		= models.ManyToManyField(Offer, related_name="offer_block", blank=True)


	def get_cut_amounts(self):
		"""
		Return the user's party cut amounts.
		Set user to party if not already in one.
		"""
		if not self.party:
			self.party = self.party.get_or_create_default()
			self.save()

		return (
			Decimal(self.party.cut_amount),
			Decimal(self.party.referral_cut_amount)
		)



class Earnings(EarningsBase):
	"""
	Earnings model for User's earnings.
	"""
	parent = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)


	class Meta:
		verbose_name_plural = "Earnings"



class ReferralEarnings(EarningsBase):
	"""
	Earnings model for User's referred earnings.
	"""
	parent = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)


	class Meta:
		verbose_name = "Referral Earnings"
		verbose_name_plural = "Referral Earnings"