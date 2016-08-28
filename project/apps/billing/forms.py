import json
from django import forms


class Form_Billing_Base(forms.Form):
	@classmethod
	def from_request(cls, request, **kwargs):
		""" Create form from request """
		prefix = cls.__name__[5:].lower()
		choice = prefix.upper()

		# Billing data
		data = request.user.billing.data
		if not isinstance(data, dict):
			data = json.loads(data or "{}")

		# POST data and initial data
		post = request.POST if request.POST.get("form") == choice else None
		initial = data[choice] if (choice in data) else {}

		# Form
		form = cls(post, initial=initial, prefix=prefix, **kwargs)
		form.choice = choice
		form.user = request.user

		return form


	def save(self):
		""" Save billing details """
		if not self.is_valid():
			return False

		# Method
		billing = self.user.billing
		billing.choice = self.choice

		# Data
		try:
			data = json.loads(billing.data)
		except:
			data = {}

		data[self.choice] = self.cleaned_data

		billing.data = json.dumps(data)
		billing.save()
		return True


TEXTAREA_ATTRS = {
	"required": False,
	"max_length": 500,
	"widget": forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}),
}


class Form_Paypal(Form_Billing_Base):
	""" Billing form for Paypal """
	email = forms.EmailField(label="Paypal E-mail")


class Form_Check(Form_Billing_Base):
	""" Billing form for Checks """	
	pay_to 	= forms.CharField(max_length=100, label="Pay To")
	address	= forms.CharField(
		required=False, max_length=300,
		widget=forms.Textarea(attrs=TEXTAREA_ATTRS))


class Form_Wire(Form_Billing_Base):
	""" Billing form for Wire transfers """
	beneficiary_name 	= forms.CharField(max_length=100, label="Beneficiary Name")
	bank_name 			= forms.CharField(max_length=100, label="Bank Name")
	account_number		= forms.CharField(max_length=100, label="Account Number")
	routing_aba_swift 	= forms.CharField(max_length=100, label="Routing Number")
	bank_address 		= forms.CharField(label="Bank Address", **TEXTAREA_ATTRS)
	additional 			= forms.CharField(label="Additional Information", **TEXTAREA_ATTRS)


class Form_Direct(Form_Billing_Base):
	""" Billing form for Direct transfers """
	account_holder 	= forms.CharField(max_length=100, label="Account Holder")
	bank_name 		= forms.CharField(max_length=100, label="Bank Name")
	account_number 	= forms.CharField(max_length=100, label="Account Number")
	routing_number 	= forms.CharField(max_length=100, label="Routing Number")
	additional 		= forms.CharField(label="Additional Information", **TEXTAREA_ATTRS)