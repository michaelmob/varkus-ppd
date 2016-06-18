import json
from django import forms


class Form_Billing_Base(forms.Form):
	def __init__(self, request, **kwargs):
		prefix = self.__class__.__name__[5:].lower()
		self.choice = prefix.upper()
		self.request = request

		# User's billing data
		data = json.loads(self.request.user.billing.data or "{}")

		# POST data and initial data
		post = self.request.POST if str(request.POST.get("form")) == self.choice else None
		initial = data[self.choice] if (self.choice in data) else {}

		super(__class__, self).__init__(post,
			initial=initial, prefix=prefix, **kwargs)

	def save(self):
		if not self.is_valid():
			return False

		# Method
		billing = self.request.user.billing
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


class Form_Paypal(Form_Billing_Base):
	email = forms.EmailField(label="Paypal E-mail")


class Form_Check(Form_Billing_Base):	
	pay_to 	= forms.CharField(max_length=100, label="Pay To")
	address	= forms.CharField(
		required=False, max_length=300,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))


class Form_Wire(Form_Billing_Base):	
	beneficiary_name 	= forms.CharField(max_length=100, label="Beneficiary Name")
	bank_name 			= forms.CharField(max_length=100, label="Bank Name")
	account_number		= forms.CharField(max_length=100, label="Account Number")
	routing_aba_swift 	= forms.CharField(max_length=100, label="Routing Number")
	bank_address 		= forms.CharField(
		label="Bank Address", max_length=300,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))
	additional 		= forms.CharField(
		label="Additional Information", required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))


class Form_Direct(Form_Billing_Base):	
	account_holder 	= forms.CharField(max_length=100, label="Account Holder")
	bank_name 		= forms.CharField(max_length=100, label="Bank Name")
	account_number 	= forms.CharField(max_length=100, label="Account Number")
	routing_number 	= forms.CharField(max_length=100, label="Routing Number")
	additional 		= forms.CharField(
		label="Additional Information", required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))