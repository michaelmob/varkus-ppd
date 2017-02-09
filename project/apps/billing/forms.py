import json
from django import forms


TEXTAREA_ATTRS = {
	"required": False,
	"max_length": 500,
	"widget": forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}),
}



class BillingFormBase(forms.Form):
	"""
	Base form for Billing forms.
	"""
	name = "NONE"

	def __init__(self, data=None, *args, **kwargs):
		"""
		Do not set form data if the submitted form is not the right one.
		"""
		self.prefix = self.name.lower()
		if data and data.get("form") != self.name:
			data = None
		return super(__class__, self).__init__(data, *args, **kwargs)


	def save_user(self, user):
		"""
		Save data to User's billing profile.
		"""
		try:
			data = json.loads(user.billing.data)
		except:
			data = {}

		data[self.name] = self.cleaned_data

		user.billing.choice = self.name
		user.billing.data = json.dumps(data)
		user.billing.save()
		return True



class PaypalForm(BillingFormBase):
	"""
	Billing form for Paypal.
	"""
	name = "PAYPAL"
	email = forms.EmailField(label="Paypal E-mail")



class CheckForm(BillingFormBase):
	"""
	Billing form for Checks.
	"""	
	name = "CHECK"
	pay_to = forms.CharField(max_length=100, label="Pay To")
	address	= forms.CharField(
		required=False, max_length=300, widget=forms.Textarea(attrs=TEXTAREA_ATTRS)
	)



class WireForm(BillingFormBase):
	"""
	Billing form for Wire transfers.
	"""
	name = "WIRE"
	beneficiary_name = forms.CharField(max_length=100, label="Beneficiary Name")
	bank_name = forms.CharField(max_length=100, label="Bank Name")
	account_number = forms.CharField(max_length=100, label="Account Number")
	routing_aba_swift = forms.CharField(max_length=100, label="Routing Number")
	bank_address = forms.CharField(label="Bank Address", **TEXTAREA_ATTRS)
	additional = forms.CharField(label="Additional Information", **TEXTAREA_ATTRS)



class DirectDepositForm(BillingFormBase):
	"""
	Billing form for Direct Deposit transfers.
	"""
	name = "DIRECT"
	account_holder = forms.CharField(max_length=100, label="Account Holder")
	bank_name = forms.CharField(max_length=100, label="Bank Name")
	account_number = forms.CharField(max_length=100, label="Account Number")
	routing_number = forms.CharField(max_length=100, label="Routing Number")
	additional = forms.CharField(label="Additional Information", **TEXTAREA_ATTRS)