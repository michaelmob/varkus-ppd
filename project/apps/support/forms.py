from django import forms
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from apps.support.models import Contact_Message, Abuse_Report


class Form_Contact(ModelForm):
	captcha = ReCaptchaField(attrs={"theme": "clean"})

	class Meta:
		model = Contact_Message
		fields = ("name", "email", "subject", "message", "captcha")

	def __init__(self, request, **kwargs):
		self.request = request
		super(__class__, self).__init__(request.POST or None, **kwargs)

	def save(self):
		# Validate
		if not self.is_valid():
			return None

		# Create object
		obj = super(__class__, self).save(commit=False)

		# Set Fields
		obj.name 		= self.cleaned_data["name"]
		obj.email 		= self.cleaned_data["email"]
		obj.user 		= self.request.user if self.request.user.is_authenticated() else None
		obj.ip_address 	= self.request.META.get("REMOTE_ADDR")
		obj.subject 	= self.cleaned_data["subject"]
		obj.message 	= self.cleaned_data["message"]
		obj.save()

		return obj


class Form_Report(ModelForm):
	captcha = ReCaptchaField(attrs={"theme": "clean"})
	COMPLAINTS = (("", "Please Choose"),) + Abuse_Report.COMPLAINTS

	class Meta:
		model = Abuse_Report
		fields = ("name", "email", "complaint", "message", "file1", "file2", "file3")
		labels = {
			"message": "Content Links, Reasons and Evidence",
			"file1": "",
			"file2": "",
			"file3": "",
		}

	def __init__(self, request, **kwargs):
		self.request = request
		super(__class__, self).__init__(
			request.POST or None,
			request.FILES or None,
			initial={
				"name": "%s %s" % (
					request.user.first_name,
					request.user.last_name
				),
				"email": request.user.email
			} if request.user.is_authenticated() else {},
			**kwargs)

	def save(self):
		# Validate
		if not self.is_valid():
			return None

		# Create object
		obj = super(__class__, self).save(commit=False)

		# Set Fields
		obj.name 		= self.cleaned_data["name"]
		obj.email 		= self.cleaned_data["email"]
		obj.user 		= self.request.user if self.request.user.is_authenticated() else None
		obj.ip_address 	= self.request.META.get("REMOTE_ADDR")
		obj.complaint 	= self.cleaned_data["complaint"]
		obj.message 	= self.cleaned_data["message"]
		obj.save()

		return obj
