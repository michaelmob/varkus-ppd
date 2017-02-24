from random import randint, uniform

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from viking.utils import constants, geoip, strings
from conversions.models import Conversion, Token
from offers.models import Offer



class Command(BaseCommand):
	"""
	Create randomized token.

	Example usage:
		./viking manage randomtoken LOCKER ID [--chance=0.25] [--count=1]
	"""

	help = "Creates randomized token(s)."


	def add_arguments(self, parser):
		"""
		Arguments for command.
		"""
		parser.add_argument("locker", type=str, help="locker's name")
		parser.add_argument("id", type=int, help="locker's object id")
		parser.add_argument("--chance", default=0.25, type=float, help="conversion chance")
		parser.add_argument("--count", default=1, type=int)
		parser.add_argument("--ip", default=1, type=str)


	def handle(self, *args, **options):
		"""
		Handle command to create the token.
		"""
		# Get model
		name = options["locker"].title()
		if not self.get_model(name):
			self.stdout.write(self.style.ERROR("Invalid locker '%s'." % name))
			return

		# Get locker object
		id = options["id"]
		if not self.get_object(id):
			self.stdout.write(self.style.ERROR("%s does not exist." % name))
			return

		self.user_ip_address = options.get("ip", None)

		print()
		for x in range(options.get("count", 1)):
			print("%d/%d:" % (x+1, options.get("count", 1)))
			self.run(*args, **options)


	def run(self, *args, **options):
		"""
		Run token creation command.
		"""
		# Create Token
		self.token = self.create_token()

		if not self.token:
			self.stdout.write(self.style.ERROR("Token was not created."))
		else:
			self.stdout.write(self.style.SUCCESS("Token has been created."))

		self.stdout.write("\tIP Address: %s (%s)" % (self.ip_address, self.country_code))

		if not self.token:
			return print()

		# Roll for chance of conversion
		roll = uniform(0, 0.9)
		chance = options.get("chance", 0.25)
		if roll > chance:
			self.stdout.write(
				"\tUnsuccessful conversion roll. (%.2f > %.2f)" % (roll, chance)
			)
		else:
			self.create_conversion(self.token)
			if self.conversion:
				self.stdout.write(
					"\tConversion has been created. ($%.2f)" % (self.conversion.payout,)
				)

		print()  # New line


	def create_token(self):
		"""
		Create the token.
		"""
		# Create random details such as IP address and country code
		self.random_identifiers()

		# Get offer
		self.get_offer()

		if not self.offer:
			return

		# Create token
		self.token = Token.objects.create(
			unique 		= strings.random(64),
			session 	= None,

			user 		= self.object.user,
			locker 		= self.object,

			ip_address 	= self.ip_address,
			user_agent 	= self.get_user_agent(),
			country 	= self.country_code
		)

		# Add offer to token
		self.token.offers.add(self.offer)

		# Increment clicks
		# Using F expressions (in this) makes this increment by 'incr number' * 2.
		# This would only be used in debugging situations so no harm.
		for earnings in (
			self.offer.earnings, self.object.user.earnings, self.object.earnings
		):
			earnings.clicks += 1
			earnings.clicks_today += 1
			earnings.save()

		return self.token


	def create_conversion(self, token):
		"""
		Create conversion for token.
		"""
		now = token.datetime.replace(
			hour=randint(token.datetime.hour, 23),
			minute=randint(token.datetime.second, 59),
			second=randint(token.datetime.second, 59)
		)

		self.conversion, created = Conversion.objects.get_or_create_conversion(
			token, datetime=now, seconds=randint(10, 300)
		)

		# For whatever reason, signals seem to be called twice in the cli
		# we need to remove the earnings to balance it out. This should only
		# be used in a debugging environment so no data races should occur
		earnings = self.conversion.user.earnings
		earnings.today -= self.conversion.payout
		earnings.week -= self.conversion.payout
		earnings.month -= self.conversion.payout
		earnings.year -= self.conversion.payout
		earnings.total -= self.conversion.payout
		earnings.save()


	def get_model(self, name):
		"""
		Get locker model the locker's name.
		"""
		if name.upper() not in dict(settings.LOCKERS).keys():
			return

		try:
			self.model = apps.get_model("lockers", name.title())
		except LookupError:
			return

		return self.model


	def get_object(self, id):
		"""
		Get locker object with the model and its id.
		"""
		try:
			self.object = self.model.objects.get(id=id)
		except self.model.DoesNotExist:
			return

		return self.object


	def get_offer(self, attempts=0):
		"""
		Get random offer.
		"""
		if attempts > 4:
			return self.offer

		self.offer = (
			Offer.objects
				.filter(
					earnings_per_click__gt=0.01,
					countries__contains=self.country_code.upper()
				)
				.order_by("?")
				.first()
		)

		if not self.offer:
			return self.get_offer(attempts + 1)


	def get_user_agent(self):
		"""
		Get random user agent from list of user agents.
		"""
		return constants.USER_AGENTS[randint(0, len(constants.USER_AGENTS) - 1)]


	def random_identifiers(self):
		"""
		Roll for country code from random real IP address.
		"""
		self.country_code = None

		# Random, but valid, IP Address and country
		while not self.country_code:
			if self.user_ip_address:
				self.ip_address = self.user_ip_address
				self.user_ip_address = None
			else:
				self.ip_address = ".".join(str(randint(0, 255)) for n in range(4))

			try:
				self.country_code = geoip.country_code(self.ip_address)
			except:
				print("No country found")
				self.country_code = None


	def datetime(self):
		"""
		Create datetime of today and randomize hours and minutes.
		"""
		return datetime.now().replace(hour=randint(0, 23), minute=randint(0, 59))