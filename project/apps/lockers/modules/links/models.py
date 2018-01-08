from django.db import models
from lockers.models import LockerBase, EarningsBase



class Link(LockerBase):
	"""
	Model for Link locker.
	"""
	url = models.URLField(max_length=1000, verbose_name="URL")
	proxy = models.BooleanField(default=False)


	@classmethod
	def get_earnings_model(cls):
		"""
		Return earnings model for Link.
		"""
		return LinkEarnings



class LinkEarnings(EarningsBase):
	"""
	Model for Link's earnings.
	"""
	parent = models.OneToOneField(Link, primary_key=True, on_delete=models.CASCADE)


	class Meta:
		default_related_name = "earnings"