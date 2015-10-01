from django.shortcuts import render
from ..models import Invoice, Billing, PAYMENT_CHOICES_USER_DICT
from ..forms import Form_Paypal, Form_Check, Form_Wire, Form_Direct

from ..tables import Table_Invoice


def overview(request, page=1):
	Billing.objects.get_or_create(user=request.user)

	if request.user.profile.notification_billing > 0:
		request.user.profile.notification_billing = 0
		request.user.profile.save()

	info 	= request.user.billing
	forms 	= __overview_forms(request.POST or None, info)

	if request.POST:
		__overview_modify(request.POST or None, forms, info)

	table = Table_Invoice.create(request)

	return render(request, "billing/overview.html", {
		"payment_choices":	PAYMENT_CHOICES_USER_DICT,
		"table":			table,
		"form_paypal":		forms["paypal"],
		"form_check":		forms["check"],
		"form_wire":		forms["wire"],
		"form_direct":		forms["direct"]
	})


def __overview_forms(post, info):
	forms = {}

	forms["paypal"] = Form_Paypal(
		post,
		initial={
			"paypal_email": 			info.paypal_email
		}
	)

	forms["check"] = Form_Check(
		post,
		initial={
			"check_pay_to": 			info.check_pay_to,
			"check_address":			info.check_address
		}
	)

	forms["wire"] = Form_Wire(
		post,
		initial={
			"wire_beneficiary_name": 	info.wire_beneficiary_name,
			"wire_account_number": 		info.wire_account_number,
			"wire_bank_name": 			info.wire_bank_name,
			"wire_routing_aba_swift": 	info.wire_routing_aba_swift,
			"wire_bank_address": 		info.wire_bank_address,
			"wire_additional":	 		info.wire_additional
		}
	)

	forms["direct"] = Form_Direct(
		post,
		initial={
			"direct_account_holder": 	info.direct_account_holder,
			"direct_account_number": 	info.direct_account_number,
			"direct_routing_number": 	info.direct_routing_number,
			"direct_bank_name": 		info.direct_bank_name,
			"direct_additional": 		info.direct_additional
		}
	)

	return forms

def __overview_modify(post, forms, info):
	method = post.get("payment_method")

	if method == "paypal":
		if forms["paypal"].is_valid():
			info.paypal_email 			= forms["paypal"].cleaned_data["paypal_email"]
			info.method					= method
		else:
			pass

	elif method == "check":
		if forms["check"].is_valid():
			info.check_pay_to 			= forms["check"].cleaned_data["check_pay_to"]
			info.check_address 			= forms["check"].cleaned_data["check_address"]
			info.method					= method
		else:
			pass

	elif method == "wire":
		if forms["wire"].is_valid():
			info.wire_beneficiary_name 	= forms["wire"].cleaned_data["wire_beneficiary_name"]
			info.wire_account_number		= forms["wire"].cleaned_data["wire_account_number"]
			info.wire_bank_name			= forms["wire"].cleaned_data["wire_bank_name"]
			info.wire_routing_aba_swift	= forms["wire"].cleaned_data["wire_routing_aba_swift"]
			info.wire_bank_address		= forms["wire"].cleaned_data["wire_bank_address"]
			info.wire_additional			= forms["wire"].cleaned_data["wire_additional"]
			info.method					= method
		else:
			pass

	elif method == "direct":
		if forms["direct"].is_valid():
			info.direct_account_holder	= forms["direct"].cleaned_data["direct_account_holder"]
			info.direct_account_number	= forms["direct"].cleaned_data["direct_account_number"]
			info.direct_routing_number	= forms["direct"].cleaned_data["direct_routing_number"]
			info.direct_bank_name		= forms["direct"].cleaned_data["direct_bank_name"]
			info.direct_additional		= forms["direct"].cleaned_data["direct_additional"]
			info.method					= method
		else:
			pass

	info.save()


def invoice(request):

	return render(request, "billing/invoice.html", {})
