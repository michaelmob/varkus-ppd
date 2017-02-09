from decimal import Decimal
from datetime import datetime, timedelta
from django.apps import apps
from django.db import models
from viking.utils import strings
from viking.utils.geoip import country_code



class TokenManager(models.Manager):
	"""
	Manager for Token model.
	"""
	def clear(self, days=30):
		"""
		Clear tokens older than `days`.
		"""
		return self.filter(
			datetime__lt=datetime.now() - timedelta(days=days)
		).delete()


	def get_token(self, request, locker_object):
		"""
		Return user-associated Token.
		"""
		return self.filter(
			ip_address=request.META.get("REMOTE_ADDR"), **locker_object.filter_args()
		).first()


	def get_or_create_token(self, request, locker_object, offer_object=None):
		"""
		Return user-associated Token, creating it if it does not already exist.
		"""
		token = self.get_token(request, locker_object)
		created = False

		if not token:
			token = self.create(
				unique 		= strings.random(64),
				session 	= request.session.session_key,
				user 		= locker_object.user,
				locker 		= locker_object,
				ip_address 	= request.META.get("REMOTE_ADDR"),
				user_agent 	= request.META.get("HTTP_USER_AGENT"),
				country 	= country_code(request.META.get("REMOTE_ADDR")) or "XX"
			)
			created = True
		else:
			token.last_access = datetime.now()
			token.save()

		if offer_object:
			token.offers.add(offer_object)

		return (token, created)



class ConversionManager(models.Manager):
	"""
	Manager for Conversion model.
	"""
	def get_or_create_conversion(self, token, offer=None, sender=None, payout=None, **kwargs):
		"""
		Create conversion if it does not exist.
		"""
		# No offer passed so fetch last offer from `offers` field on Token
		if token and not offer:
			offer = token.offers.last()

		# No offer, just make one for the sake of it
		if not offer:
			offer = apps.get_model("offers", "Offer")()

		# Create blank token if no token
		if not token:
			token = apps.get_model("conversions", "Token")()
			token.last_access = datetime.now()

		# Values to search for existing Conversion
		filter_args = {
			"offer": offer if offer.pk else None,
			"token": token if token.pk else None,
			"user": token.user
		}

		# Attempt to find an existing conversion
		conversion = self.filter(**filter_args).first()
		if conversion:
			return (conversion, False)

		# Calculate seconds it took to complete
		now = datetime.now()
		seconds = int((now - token.last_access).total_seconds())

		# Determine payout
		payout = Decimal(payout or offer.payout)

		# Conversion does not exist
		# Creation values for conversion
		values = {
			"offer_name"			: offer.name,

			"accessor_ip_address"	: sender,
			"ip_address"			: token.ip_address,
			"user_agent" 			: token.user_agent,

			"locker"				: token.locker,

			"payout"				: payout,
			"total_payout"			: payout,

			"is_blocked"			: kwargs.get("is_blocked", False),
			"is_approved"			: kwargs.get("is_approved", True),

			"deposit"				: kwargs.get("deposit", "DEFAULT_DEPOSIT"),
			"seconds" 				: seconds,
			"datetime" 				: now,
		}

		# Update our creation values with the values we used to filter before
		values.update(filter_args)

		# Optional values
		if "datetime" in kwargs:
			values["datetime"] = kwargs["datetime"]

		if "seconds" in kwargs:
			values["seconds"] = kwargs["seconds"]

		# Find IP address country, use Offer's country if not found
		values["country"] = country_code(token.ip_address) or offer.country
		
		# Create the conversion
		return (self.create(**values), True)



class BoostManager(models.Manager):
	"""
	Manager for Boost model.
	"""
	def create_boost(self, user, offer, count=10):
		"""
		Create or update in-place boost.
		"""
		boost = self.filter(user=user, offer=offer).first()

		if boost:
			boost.count += count
			boost.save()
			return boost

		return self.create(user=user, offer=offer, count=count)