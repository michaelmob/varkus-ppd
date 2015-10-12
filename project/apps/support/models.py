from django.db import models
from django.contrib.auth.models import User


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
		verbose_name = "Contact Message"

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
		verbose_name = "Abuse Report"

	def delete(self, *args, **kwargs):
		self.image1.delete()
		self.image2.delete()
		self.image3.delete()
		super(Abuse_Report, self).delete(*args, **kwargs)

	def __str__(self):
		return "%s's complaint" % (self.email)

	name = models.CharField(max_length=100)
	email = models.EmailField()
	user = models.ForeignKey(User, default=None, blank=True, null=True)
	ip_address = models.GenericIPAddressField()
	date_time = models.DateTimeField(auto_now_add=True)
	complaint = models.CharField(max_length=100, choices=COMPLAINTS)
	text = models.TextField(max_length=5000)
	image1 = models.ImageField(upload_to="reports/%b-%Y/", default=None, blank=True, null=True)
	image2 = models.ImageField(upload_to="reports/%b-%Y/", default=None, blank=True, null=True)
	image3 = models.ImageField(upload_to="reports/%b-%Y/", default=None, blank=True, null=True)
	viewed = models.BooleanField(default=False)