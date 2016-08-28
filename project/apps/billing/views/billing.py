import json

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
		data = request.user.billing.data
		data = data if isinstance(data, dict) else json.loads(data or "{}")

		return render(request, "billing/overview.html", {
			"invoices": Table_Invoice(request),
			"choice": request.user.billing.choice,
			"data": data,

			"form_paypal": 	Form_Paypal.from_request(request),
			"form_check": 	Form_Check.from_request(request),
			"form_wire": 	Form_Wire.from_request(request),
			"form_direct": 	Form_Direct.from_request(request)
		})

	def post(self, request):
		success = False
		form = request.POST.get("form")

		# Validate choice
		if form == "PAYPAL":
			success = Form_Paypal.from_request(request).save()

		elif form == "CHECK":
			success = Form_Check.from_request(request).save()

		elif form == "WIRE":
			success = Form_Wire.from_request(request).save()

		elif form == "DIRECT":
			success = Form_Direct.from_request(request).save()

		# Success Message
		if success:
			messages.success(request, "Your billing information has been saved.")
		else:
			messages.error(request, "An error has occured. Your billing information has not been saved.")

		return self.get(request)