from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Sum
from conversions.models import Conversion


class Command(BaseCommand):
	"""
	Reset a user's earnings.

	Example usage:
		./viking manage recalculateuser 1 
	"""

	help = "Re-calculate a user's earnings."


	def add_arguments(self, parser):
		"""
		Arguments for command.
		"""
		parser.add_argument("user", type=int, help="user id")


	def filter(self, range_start, range_end=None):
		"""
		Run a Conversion filter and find Conversions in date range.
		"""
		if not range_end:
			range_end = self.range_end

		result = (
			Conversion.objects
				.filter(
					user=self.user,
					datetime__range=(range_start, range_end)
				)
				.aggregate(sum=Sum(self.field))["sum"]
			)

		return result if result else 0


	def handle(self, *args, **options):
		"""
		Handle command to reset earnings.
		"""
		self.user = User.objects.filter(id=options.get("user")).first()

		if not self.user:
			self.stdout.write(self.style.ERROR("User does not exist."))
			return

		today = datetime.now()

		# Ranges
		today_datetime = datetime(today.year, today.month, today.day)
		yesterday_datetime = today_datetime - timedelta(days=1)
		week_datetime = today_datetime - timedelta(days=today.weekday())
		month_datetime = datetime(today.year, today.month, 1)
		yestermonth_datetime = (month_datetime - timedelta(days=1)).replace(day=1)
		year_datetime = datetime(today.year, 1, 1)

		# Ending Range
		self.range_end = today_datetime + timedelta(days=1)

		# Aggregate Earnings
		self.field = "payout"
		earnings = self.user.earnings

		earnings.today = self.filter(today_datetime)
		earnings.yesterday = self.filter(yesterday_datetime, today_datetime)
		earnings.week = self.filter(week_datetime)
		earnings.month = self.filter(month_datetime)
		earnings.yestermonth = self.filter(yestermonth_datetime, month_datetime)
		earnings.year = self.filter(year_datetime)
		earnings.save()

		# Aggregate Referral Earnings
		self.field = "referral_payout"
		referral_earnings = self.user.referralearnings

		referral_earnings.today = self.filter(today_datetime)
		referral_earnings.yesterday = self.filter(yesterday_datetime, today_datetime)
		referral_earnings.week = self.filter(week_datetime)
		referral_earnings.month = self.filter(month_datetime)
		referral_earnings.yestermonth = self.filter(yestermonth_datetime, month_datetime)
		referral_earnings.year = self.filter(year_datetime)
		referral_earnings.save()

		self.stdout.write(self.style.SUCCESS(
			"User's earnings have been recalculated."
		))