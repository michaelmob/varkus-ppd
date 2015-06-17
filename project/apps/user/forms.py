from django import forms
from django_countries.fields import CountryField


class Form_Sign_Up(forms.Form):
	referrer = forms.IntegerField(widget=forms.HiddenInput(), required=False)

	# Generic
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	username = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)
	confirm = forms.CharField(max_length=32, widget=forms.PasswordInput)

	# Birthday
	day = forms.IntegerField(widget=forms.HiddenInput())
	month = forms.IntegerField(widget=forms.HiddenInput())
	year = forms.IntegerField(widget=forms.HiddenInput())


class Form_Log_In(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class Form_Password_Reset(forms.Form):
	email = forms.EmailField(max_length=100)


class Form_Personal_Details(forms.Form):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	country = forms.CharField(max_length=100)
	website = forms.URLField(max_length=100, required=False)


class Form_Account_Details(forms.Form):
	email = forms.EmailField(max_length=100)
