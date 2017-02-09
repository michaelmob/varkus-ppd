import re
from datetime import date, timedelta
from django import forms
from django.conf import settings
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django_countries import countries
from django_countries.fields import CountryField
from .models import Profile, Party



class RegistrationForm(UserCreationForm):
	"""
	Form for a User's registration.
	"""
	referrer = forms.IntegerField(required=False, label="", widget=forms.HiddenInput())
	email = forms.EmailField(required=True, label="E-mail")
	birthdate = forms.DateField()
	password2 = forms.CharField(label="Confirm", widget=forms.PasswordInput())
	agree = forms.BooleanField(
		error_messages={"required": "You must agree to the Terms and Conditions"},
		label="I agree to the <a target='_blank' href='/terms/'>Terms of Service</a>."
	)


	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email", "password1", "password2")


	def clean_username(self):
		"""
		Verify account is not using an already in use username.
		"""
		data = self.cleaned_data["username"]
		if User.objects.filter(username=data).exists():
			raise forms.ValidationError("That username is already in use.")
		return data


	def clean_email(self):
		"""
		Verify account is not using an already in use e-mail address.
		"""
		data = self.cleaned_data["email"]
		if User.objects.filter(email=data).exists():
			raise forms.ValidationError("That e-mail address is already in use.")
		return data


	def clean_birthdate(self):
		"""
		Verify account is not using an already in use e-mail address.
		"""
		t = date.today()
		b = self.cleaned_data["birthdate"]

		if (b.year + 18, b.month, b.day) > (t.year, t.month, t.day):
			raise forms.ValidationError(
				"You must be 18 years of age or older to use %s." % settings.SITE_NAME
			)

		return b


	def save(self, commit=True):
		"""
		Save the newly created user object.
		"""
		user = super(__class__, self).save(commit=False)

		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.email = self.cleaned_data["email"]

		if not commit:
			return user
		
		user.save()

		# `user_saved_signal` will create the profile
		if "referrer" in self.cleaned_data:
			user.profile.referrer = User.objects.filter(pk=self.cleaned_data["referrer"]).first()
		user.profile.birthdate = self.cleaned_data["birthdate"]
		user.profile.save()

		return user



class AccountForm(forms.Form):
	"""
	Form to update a User's details.
	"""
	first_name 	= forms.CharField(max_length=100, label="First Name")
	last_name 	= forms.CharField(max_length=100, label="Last Name")
	address 	= forms.CharField(max_length=100)
	city 		= forms.CharField(max_length=100)
	state 		= forms.CharField(max_length=100, label="State / Region")

	country 	= forms.ChoiceField(choices=countries)
	postal_code = forms.RegexField(regex=r"^[0-9]+$", max_length=100, label="Postal Code")
	phone_number = forms.RegexField(regex=r"^[0-9\+\-\ ]+$", max_length=100, label="Phone Number")

	company = forms.CharField(max_length=100, required=False)
	website = forms.URLField(max_length=100, required=False)
	email = forms.EmailField(max_length=100, label="E-mail")


	def get_initial(initial, user):
		"""
		Get initial form values from user.
		"""
		# Personal
		initial["first_name"] = user.first_name
		initial["last_name"] = user.last_name
		initial["country"] = user.profile.country
		initial["state"] = user.profile.state
		initial["city"] = user.profile.city
		initial["address"] = user.profile.address
		initial["postal_code"] = user.profile.postal_code
		initial["phone_number"] = user.profile.phone_number

		# Account
		initial["email"] = user.email
		initial["company"] = user.profile.company
		initial["website"] = user.profile.website

		return initial


	def save_user(self, user):
		"""
		Save form data to the user and profile.
		"""
		# Personal
		user.first_name = self.cleaned_data["first_name"]
		user.last_name 	= self.cleaned_data["last_name"]
		user.profile.address = self.cleaned_data["address"]
		user.profile.city = self.cleaned_data["city"]
		user.profile.state = self.cleaned_data["state"]
		user.profile.country = self.cleaned_data["country"]
		user.profile.postal_code = self.cleaned_data["postal_code"]
		user.profile.phone_number = self.cleaned_data["phone_number"]

		# Account
		user.email = self.cleaned_data["email"]
		user.profile.company = self.cleaned_data["company"]
		user.profile.website = self.cleaned_data["website"]

		user.save()
		user.profile.save()