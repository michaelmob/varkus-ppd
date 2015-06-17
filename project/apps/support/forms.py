from django import forms
from captcha.fields import ReCaptchaField
from apps.support.models import Abuse_Report


class Form_Contact(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	subject = forms.CharField(max_length=100)
	message = forms.CharField(max_length=1000, widget=forms.Textarea)
	captcha = ReCaptchaField(attrs={"theme": "clean"})



class Form_Report(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	complaint = forms.ChoiceField(choices=Abuse_Report.COMPLAINTS)
	text = forms.CharField(max_length=5000, widget=forms.Textarea)
	image1 = forms.ImageField(required=False)
	image2 = forms.ImageField(required=False)
	image3 = forms.ImageField(required=False)
	captcha = ReCaptchaField(attrs={"theme": "clean"})