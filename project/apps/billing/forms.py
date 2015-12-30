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
	request = None

	paypal_email = forms.EmailField(label="Paypal E-mail")

	def create(request):
		post = request.POST if request.POST.get("payment_method") == "paypal" else None

		form = __class__(post or None, initial={
			"paypal_email": request.user.billing.paypal_email })
		form.request = request
		return form

	def save(self):
		if not self.is_valid():
			return False

		b = self.request.user.billing
		b.paypal_email = self.cleaned_data["paypal_email"]
		b.method = "paypal"
		b.save()
		return True



class Form_Check(forms.Form):
	request = None
	
	check_pay_to 	= forms.CharField(max_length=100, label="Pay To")
	check_address	= forms.CharField(
		required=False, max_length=300,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))

	def create(request):
		post = request.POST if request.POST.get("payment_method") == "check" else None

		b = request.user.billing
		form = __class__(post or None, initial={
			"check_pay_to":		b.check_pay_to,
			"check_address": 	b.check_address })
		form.request = request
		return form

	def save(self):
		if not self.is_valid():
			print("Here", self.errors())
			return False

		b = self.request.user.billing

		b.check_pay_to 	= self.cleaned_data["check_pay_to"]
		b.check_address = self.cleaned_data["check_address"]
		b.method		= "check"
		b.save()
		return True



class Form_Wire(forms.Form):
	request = None
	
	wire_beneficiary_name 	= forms.CharField(max_length=100, label="Beneficiary Name")
	wire_bank_name 			= forms.CharField(max_length=100, label="Bank Name")
	wire_account_number 	= forms.CharField(max_length=100, label="Account Number")
	wire_routing_aba_swift 	= forms.CharField(max_length=100, label="Routing Number")
	wire_bank_address 		= forms.CharField(
		label="Bank Address", max_length=300,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))
	wire_additional 		= forms.CharField(
		label="Additional Information", required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))

	def create(request):
		post = request.POST if request.POST.get("payment_method") == "wire" else None

		b = request.user.billing
		form = __class__(post or None, initial={
			"wire_beneficiary_name": 	b.wire_beneficiary_name,
			"wire_account_number": 		b.wire_account_number,
			"wire_bank_name": 			b.wire_bank_name,
			"wire_routing_aba_swift": 	b.wire_routing_aba_swift,
			"wire_bank_address": 		b.wire_bank_address,
			"wire_additional":	 		b.wire_additional })
		form.request = request
		return form

	def save(self):
		if not self.is_valid():
			return False

		b = self.request.user.billing

		b.wire_beneficiary_name 	= self.cleaned_data["wire_beneficiary_name"]
		b.wire_account_number		= self.cleaned_data["wire_account_number"]
		b.wire_bank_name			= self.cleaned_data["wire_bank_name"]
		b.wire_routing_aba_swift	= self.cleaned_data["wire_routing_aba_swift"]
		b.wire_bank_address			= self.cleaned_data["wire_bank_address"]
		b.wire_additional			= self.cleaned_data["wire_additional"]
		b.method					= "wire"
		b.save()
		return True



class Form_Direct(forms.Form):
	request = None
	
	direct_account_holder 	= forms.CharField(max_length=100, label="Account Holder")
	direct_bank_name 		= forms.CharField(max_length=100, label="Bank Name")
	direct_account_number 	= forms.CharField(max_length=100, label="Account Number")
	direct_routing_number 	= forms.CharField(max_length=100, label="Routing Number")
	direct_additional 		= forms.CharField(
		label="Additional Information", required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"}))

	def create(request):
		post = request.POST if request.POST.get("payment_method") == "direct" else None

		b = request.user.billing
		form = __class__(post or None, initial={
			"direct_account_holder": 	b.direct_account_holder,
			"direct_bank_name": 		b.direct_bank_name,
			"direct_account_number": 	b.direct_account_number,
			"direct_routing_number": 	b.direct_routing_number,
			"direct_additional": 		b.direct_additional })
		form.request = request
		return form

	def save(self):
		if not self.is_valid():
			return False

		b = self.request.user.billing

		b.direct_account_holder	= self.cleaned_data["direct_account_holder"]
		b.direct_bank_name		= self.cleaned_data["direct_bank_name"]
		b.direct_account_number	= self.cleaned_data["direct_account_number"]
		b.direct_routing_number	= self.cleaned_data["direct_routing_number"]
		b.direct_additional		= self.cleaned_data["direct_additional"]
		b.method				= "direct"
		b.save()
		return True