from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.constants import DEFAULT_BLANK_NULL


class Contact_Message(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	user = models.ForeignKey(User, **DEFAULT_BLANK_NULL)
	ip_address = models.GenericIPAddressField()
	datetime = models.DateTimeField(auto_now_add=True)
	subject = models.CharField(max_length=100)
	message = models.TextField(max_length=1000)
	unread = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Contact message"

	def __str__(self):
		return "%s's message" % (self.email)


class Abuse_Report(models.Model):
	COMPLAINTS = (
		("copyright", "Copyrighted File"),
		("porn", "Pornography"),
		("child", "Child Pornography"),
		("spam", "Spammed Link"),
		("other", "Other Complaint"),
	)

	class Meta:
		verbose_name = "Abuse report"

	def validate_file(field):
		if field.file.size > settings.REPORT_MAX_FILE_SIZE:
			raise ValidationError("File size must be less than 4mb!")

	name = models.CharField(max_length=100)
	email = models.EmailField()
	user = models.ForeignKey(User, default=None, blank=True, null=True)
	ip_address = models.GenericIPAddressField()
	datetime = models.DateTimeField(auto_now_add=True)
	complaint = models.CharField(max_length=100, choices=COMPLAINTS)
	message = models.TextField(max_length=5000)
	file1 = models.FileField(upload_to="reports/%Y/%m/%d/", validators=[validate_file], **DEFAULT_BLANK_NULL)
	file2 = models.FileField(upload_to="reports/%Y/%m/%d/", validators=[validate_file], **DEFAULT_BLANK_NULL)
	file3 = models.FileField(upload_to="reports/%Y/%m/%d/", validators=[validate_file], **DEFAULT_BLANK_NULL)
	unread = models.BooleanField(default=True)

	def delete(self, *args, **kwargs):
		self.file1.delete()
		self.file2.delete()
		self.file3.delete()
		super(__class__, self).delete(*args, **kwargs)

	def __str__(self):
		return "%s's complaint" % (self.email)
