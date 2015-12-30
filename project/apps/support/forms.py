from django import forms
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from apps.support.models import Contact_Message, Abuse_Report


class Form_Contact(ModelForm):
	captcha = ReCaptchaField(attrs={"theme": "clean"})

	class Meta:
		model = Contact_Message
		fields = ("name", "email", "subject", "message", "captcha")

	def create(self, request):
		obj = super(__class__, self).save(commit=False)

		# Set Fields
		obj.name 		= self.cleaned_data["name"]
		obj.email 		= self.cleaned_data["email"]
		obj.user 		= request.user if request.user.is_authenticated() else None
		obj.ip_address 	= request.META.get("REMOTE_ADDR")
		obj.subject 	= self.cleaned_data["subject"]
		obj.message 	= self.cleaned_data["message"]
		obj.save()

		return obj


class Form_Report(ModelForm):
	captcha = ReCaptchaField(attrs={"theme": "clean"})
	COMPLAINTS = (("", "Please Choose"),) + Abuse_Report.COMPLAINTS

	#complaint = forms.ChoiceField(choices=COMPLAINTS, widget=forms.Select(attrs={"class": "ui fluid compact dropdown"}))

	class Meta:
		model = Abuse_Report
		fields = ("name", "email", "complaint", "message", "image1", "image2", "image3")
		labels = {
            "message": "Content Links, Reasons and Evidence",
            "image1": "",
            "image2": "",
            "image3": "",
        }

	def create(self, request):
		if not self.is_valid():
			return None

		obj = super(__class__, self).save(commit=False)

		# Set Fields
		obj.name 		= self.cleaned_data["name"]
		obj.email 		= self.cleaned_data["email"]
		obj.user 		= request.user if request.user.is_authenticated() else None
		obj.ip_address 	= request.META.get("REMOTE_ADDR")
		obj.complaint 	= self.cleaned_data["complaint"]
		obj.message 	= self.cleaned_data["message"]
		obj.save()

		return obj
