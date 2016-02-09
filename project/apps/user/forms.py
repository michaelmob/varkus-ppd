from datetime import date

from django import forms
from django.conf import settings
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django_countries import countries
from django_countries.fields import CountryField
from .models import Party

YEARS = range(date.today().year, 1900, -1)

class Form_Sign_Up(UserCreationForm):
	referrer 	= forms.IntegerField(widget=forms.HiddenInput(), label="", required=False)
	name 		= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name"}), label="")
	username 	= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}), label="")
	email 		= forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "E-mail"}), label="")
	password1 	= forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}), label="")
	password2 	= forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}), label="")
	birthday 	= forms.DateField(widget=SelectDateWidget(years=YEARS, attrs={"class": "ui fluid compact dropdown"}), label="Birthday <small>This is permanent!</small>")
	agree 		= forms.BooleanField(error_messages={"required": "You must agree to the Terms and Conditions"},
		label="I agree to the <a target='_blank' href='/terms/'>Terms of Service</a>.")

	class Meta:
		model = User
		fields = (
			"name", "username", "email",
			"password1", "password2",
			"birthday", "agree"
		)

	def create(self):
		# Validation
		if not self.is_valid():
			return None

		# Age
		t = date.today()
		b = self.cleaned_data["birthday"]

		if(b.year + 18, b.month, b.day) > (t.year, t.month, t.day):
			self.add_error("birthday", "You must be 18 years or older to use %s." % settings.SITE_NAME)
			return None

		# E-mail Exists
		exists = User.objects.filter(email=self.cleaned_data["email"]).exists()

		if exists:
			self.add_error("email", "E-mail address is already in use")
			return None

		# Username Exists
		exists = User.objects.filter(username=self.cleaned_data["username"]).exists()

		if exists:
			self.add_error("username", "Username is already in use")
			return None

		# Create Object
		user = super(Form_Sign_Up, self).save(commit=False)

		# Split input name into Firstname, and Lastname
		name = self.cleaned_data["name"].split(" ")
		if len(name) < 2:
			name.append(" ")

		# User Fields
		user.is_active = not settings.INVITE_ONLY
		user.first_name = name[0]
		user.last_name = " ".join(name[1:])
		user.email = self.cleaned_data["email"]
		user.save()

		# User profile
		user.profile.party = Party.default()
		user.profile.birthday = self.cleaned_data["birthday"]
		user.profile.save()

		# Debug, set first user to staff
		if settings.DEBUG and user.id == 1:
			user.is_superuser = True
			user.is_staff = True
			user.save()

		return user


class Form_Password_Reset(forms.Form):
	email = forms.EmailField(max_length=100)


class Form_Personal_Details(forms.Form):
	request = None

	first_name 	= forms.CharField(max_length=100, label="First Name")
	last_name 	= forms.CharField(max_length=100, label="Last Name")
	address 	= forms.CharField(max_length=100)
	city 		= forms.CharField(max_length=100)
	state 		= forms.CharField(max_length=100, label="State / Region")

	country 		= forms.ChoiceField(choices=countries)
	postal_code 	= forms.RegexField(regex=r"^[0-9]+$", max_length=100, label="Postal Code")
	phone_number 	= forms.RegexField(regex=r"^[0-9\+\-\ ]+$", max_length=100, label="Phone Number")

	def create(request):
		user = request.user
		form = __class__(request.POST or None, initial={
			"first_name": 	user.first_name,
			"last_name": 	user.last_name,
			"address": 		user.profile.address,
			"city": 		user.profile.city,
			"state": 		user.profile.state,
			"country": 		user.profile.country,
			"postal_code": 	user.profile.postal_code,
			"phone_number": user.profile.phone_number,
		})
		form.request = request
		return form

	def save(self):
		if not self.is_valid():
			return False

		user = self.request.user

		user.first_name = self.cleaned_data["first_name"]
		user.last_name 	= self.cleaned_data["last_name"]
		user.save()

		user.profile.address 		= self.cleaned_data["address"]
		user.profile.city 			= self.cleaned_data["city"]
		user.profile.state 			= self.cleaned_data["state"]
		user.profile.country 		= self.cleaned_data["country"]
		user.profile.postal_code 	= self.cleaned_data["postal_code"]
		user.profile.phone_number 	= self.cleaned_data["phone_number"]
		user.profile.save()

		return True


class Form_Account_Details(forms.Form):
	request = None

	company = forms.CharField(max_length=100, required=False)
	website = forms.URLField(max_length=100, required=False)
	email = forms.EmailField(max_length=100,  label="E-mail")

	def create(request):
		user = request.user
		form = __class__(request.POST or None, initial={
			"company": user.profile.company,
			"website": user.profile.website,
			"email": user.email
		})

		form.request = request
		return form

	def save(self):
		if not self.is_valid():
			return False

		user = self.request.user

		user.email = self.cleaned_data["email"]
		user.save()

		user.profile.company = self.cleaned_data["company"]
		user.profile.website = self.cleaned_data["website"]
		user.profile.save()

		return True