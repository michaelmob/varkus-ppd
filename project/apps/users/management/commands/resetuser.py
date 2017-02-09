from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from conversions.models import Conversion


class Command(BaseCommand):
	"""
	Reset a user's earnings.

	Example usage:
		./viking manage resetuser 1 
	"""

	help = "Reset a user's earnings."


	def add_arguments(self, parser):
		"""
		Arguments for command.
		"""
		parser.add_argument("user", type=int, help="user id")
		parser.add_argument("--delete", type=bool, help="delete conversions")


	def handle(self, *args, **options):
		"""
		Handle command to reset earnings.
		"""
		user = User.objects.filter(id=options.get("user")).first()

		if not user:
			self.stdout.write(self.style.ERROR("User does not exist."))
			return

		if options.get("delete"):
			self.stdout.write(self.style.SUCCESS("Conversions deleted."))
			Conversion.objects.filter(user=user).delete()

		user.earnings.clicks = 0
		user.earnings.conversions = 0
		user.earnings.clicks_today = 0
		user.earnings.conversions_today = 0
		user.earnings.today = 0
		user.earnings.yesterday = 0
		user.earnings.week = 0
		user.earnings.month = 0
		user.earnings.yestermonth = 0
		user.earnings.year = 0
		user.earnings.total = 0
		user.earnings.save()

		self.stdout.write(self.style.SUCCESS("User has been reset."))