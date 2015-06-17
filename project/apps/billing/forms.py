from django import forms
from captcha.fields import ReCaptchaField
from apps.support.models import Abuse_Report


"""
	These are in different classes so the .is_valid() function can work
	and not verify the things that are not needed but put into the same
	form. They also have "name_" prefixes because "*account_number" are
	used twice for Wire and Direct and caused collisions.
"""


class Form_Paypal(forms.Form):
	paypal_email = forms.EmailField()


class Form_Check(forms.Form):
	check_pay_to 	= forms.CharField(max_length=100)

	check_address	= forms.CharField(
		required=False, max_length=300,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)


class Form_Wire(forms.Form):
	wire_beneficiary_name 	= forms.CharField(max_length=100)
	wire_account_number 		= forms.CharField(max_length=100)
	wire_bank_name 			= forms.CharField(max_length=100)
	wire_routing_aba_swift 	= forms.CharField(max_length=100)

	wire_bank_address 		= forms.CharField(
		required=False, max_length=300,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)

	wire_additional 			= forms.CharField(
		required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)


class Form_Direct(forms.Form):
	direct_account_holder 	= forms.CharField(max_length=100)
	direct_account_number 	= forms.CharField(max_length=100)
	direct_routing_number 	= forms.CharField(max_length=100)
	direct_bank_name 		= forms.CharField(max_length=100)

	direct_additional 		= forms.CharField(
		required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)
