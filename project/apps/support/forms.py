from django import forms
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from support.models import ContactMessage, AbuseReport



class ContactMessageForm(ModelForm):
	"""
	Form for sending contact messages to site staff.
	"""
	captcha = ReCaptchaField(attrs={"theme": "clean"})


	class Meta:
		model = ContactMessage
		fields = ("name", "email", "subject", "message", "captcha")



class AbuseReportForm(ModelForm):
	"""
	Form for reporting service abuse.
	"""
	message = forms.CharField(
		label="Content Links, Reasons and Evidence",
		widget=forms.Textarea(attrs={"rows": "10"})
	)
	captcha = ReCaptchaField(attrs={"theme": "clean"})


	class Meta:
		model = AbuseReport
		fields = ("name", "email", "complaint", "message", "file1", "file2", "file3")