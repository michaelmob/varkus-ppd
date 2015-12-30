from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse

from ..models import Invoice, Billing, PAYMENT_CHOICE_LIST
from ..forms import Form_Paypal, Form_Check, Form_Wire, Form_Direct
from ..tables import Table_Invoice


class View_Overview(View):
	def get(self, request):
		return render(request, "billing/overview.html", {
			"invoices": Table_Invoice.create(request),
			"payment_choices": PAYMENT_CHOICE_LIST,

			"form_paypal": 	Form_Paypal.create(request),
			"form_check": 	Form_Check.create(request),
			"form_wire": 	Form_Wire.create(request),
			"form_direct": 	Form_Direct.create(request)
		})

	def post(self, request):
		method = str(request.POST.get("payment_method"))

		if method in PAYMENT_CHOICE_LIST:
			success = eval("Form_" + method.title()).create(request).save()
		else:
			success = False

		# Success Message
		if success:
			messages.success(request, "Your billing information has been saved.")
		else:
			messages.error(request, "An error has occured. Your billing information has not been saved.")

		return self.get(request)