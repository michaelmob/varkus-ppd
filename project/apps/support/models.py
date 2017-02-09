from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from viking.utils.constants import DEFAULT_BLANK_NULL
from .constants import FILE_KWARGS



class ContactMessage(models.Model):
	"""
	Model for Contact Messages.
	"""
	name = models.CharField(max_length=100)
	email = models.EmailField()
	ip_address = models.GenericIPAddressField()
	subject = models.CharField(max_length=100)
	message = models.TextField(max_length=1000)
	unread = models.BooleanField(default=True)
	datetime = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name = "Contact message"


	def __str__(self):
		"""
		Contact Message's string representitive.
		"""
		return "%s's message" % (self.email)



class AbuseReport(models.Model):
	"""
	Model for Abuse Reports
	"""
	COMPLAINTS = (
		("COPYRIGHT", "Copyrighted File"),
		("PORN", "Pornography"),
		("CHILD", "Child Pornography"),
		("SPAM", "Spammed Link"),
		("OTHER", "Other Complaint"),
	)

	name = models.CharField(max_length=100)
	email = models.EmailField()
	ip_address = models.GenericIPAddressField()
	complaint = models.CharField(max_length=100, choices=COMPLAINTS)
	message = models.TextField(max_length=5000)
	file1 = models.FileField(**FILE_KWARGS)
	file2 = models.FileField(**FILE_KWARGS)
	file3 = models.FileField(**FILE_KWARGS)
	unread = models.BooleanField(default=True)
	datetime = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name = "Abuse report"


	def validate_file(self, field):
		"""
		Validate file is not too large.
		"""
		pass


	def __str__(self):
		"""
		Abuse Report's string representitive.
		"""
		return "%s's complaint" % (self.email)