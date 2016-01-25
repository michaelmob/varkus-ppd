from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Contact_Message(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	user = models.ForeignKey(User, default=None, blank=True, null=True)
	ip_address = models.GenericIPAddressField()
	date_time = models.DateTimeField(auto_now_add=True)
	subject = models.CharField(max_length=100)
	message = models.TextField(max_length=1000)
	viewed = models.BooleanField(default=False)

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

	def validate_image(field):
		if field.file.size > settings.REPORT_MAX_FILE_SIZE:
			raise ValidationError("File size must be less than 4mb!")

	name = models.CharField(max_length=100)
	email = models.EmailField()
	user = models.ForeignKey(User, default=None, blank=True, null=True)
	ip_address = models.GenericIPAddressField()
	date_time = models.DateTimeField(auto_now_add=True)
	complaint = models.CharField(max_length=100, choices=COMPLAINTS)
	message = models.TextField(max_length=5000)
	image1 = models.ImageField(upload_to="reports/%b-%Y/", validators=[validate_image], default=None, blank=True, null=True)
	image2 = models.ImageField(upload_to="reports/%b-%Y/", validators=[validate_image], default=None, blank=True, null=True)
	image3 = models.ImageField(upload_to="reports/%b-%Y/", validators=[validate_image], default=None, blank=True, null=True)
	viewed = models.BooleanField(default=False)

	def delete(self, *args, **kwargs):
		self.image1.delete()
		self.image2.delete()
		self.image3.delete()
		super(Abuse_Report, self).delete(*args, **kwargs)

	def __str__(self):
		return "%s's complaint" % (self.email)
