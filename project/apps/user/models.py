from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries.fields import CountryField

from ..offers.models import Offer
from ..cp.models import Earnings_Base
from apps.billing.models import Billing


class Party(models.Model):
	name = models.CharField(max_length=50)

	minimum_payout = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		default="10.00")

	cut_amount = models.DecimalField(
		validators=[MinValueValidator(0), MaxValueValidator(1)],
		max_digits=5,
		decimal_places=2,
		default="0.30",
		help_text="This percentage is taken off of the users payout -- The developers cut")

	referral_cut_amount = models.DecimalField(
		validators=[MinValueValidator(0), MaxValueValidator(1)],
		max_digits=5,
		decimal_places=2,
		default="0.10",
		help_text="This and cut_amount should not sum up to be more than 100% (or 1)")

	def initiate():
		""" Initiate default party """
		try:
			party, created = Party.objects.get_or_create(
				name=settings.DEFAULT_PARTY_NAME,
				defaults={
					"cut_amount": settings.DEFAULT_CUT_AMOUNT,
					"referral_cut_amount": settings.DEFAULT_REFERRAL_CUT_AMOUNT
				}
			)
			return True
		except:
			return False

	def default():
		return Party.objects.get(id=settings.DEFAULT_PARTY_ID)

	def __str__(self):
		return self.name

	class Meta:
		app_label = "auth"
		verbose_name_plural = "Parties"


class Profile(models.Model):
	user 			= models.OneToOneField(User, primary_key=True)
	party 			= models.ForeignKey(Party, blank=True, null=True, default=None)
	referrer 		= models.ForeignKey(User, related_name="referrer_id", blank=True, null=True, default=None)

	phone_number	= models.CharField(max_length=100, blank=True, null=True)
	address			= models.TextField(max_length=200, blank=True, null=True)
	city			= models.CharField(max_length=100, blank=True, null=True)
	state			= models.CharField(max_length=100, blank=True, null=True)
	country			= CountryField()
	postal_code		= models.CharField(max_length=20, blank=True, null=True)

	company 		= models.CharField(max_length=100, blank=True, null=True)
	website			= models.URLField(max_length=100, blank=True, null=True)
	birthday		= models.DateField(blank=True, null=True)

	offer_priority	= models.ManyToManyField(Offer, related_name="offer_priority", blank=True)
	offer_block		= models.ManyToManyField(Offer, related_name="offer_block", blank=True)

	notification_conversion = models.IntegerField(default=0)
	notification_billing 	= models.IntegerField(default=0)


class Earnings(Earnings_Base):
	obj 		= models.OneToOneField(User, primary_key=True)
	wallet		= models.DecimalField(default=Decimal(0.00), max_digits=10, decimal_places=2)

	class Meta:
		verbose_name_plural = "Earnings"


class Referral_Earnings(Earnings_Base):
	obj 		= models.OneToOneField(User, primary_key=True)

	def referrals(self):
		return User.objects.filter(profile__referrer=self.obj)

	class Meta:
		verbose_name = "Referral Earnings"
		verbose_name_plural = "Referral Earnings"


def create_user(sender, instance, created, **kwargs):
	if created:
		Profile.objects.get_or_create(user=instance)
		Billing.objects.get_or_create(user=instance)
		Earnings.objects.get_or_create(obj=instance)
		Referral_Earnings.objects.get_or_create(obj=instance)


post_save.connect(create_user, sender=User, dispatch_uid="create_user_profile")
