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
		return render(request, "billing/overview.html", {
			"invoices": Table_Invoice(request),
			"choice": request.user.billing.choice,
			"data": json.loads(request.user.billing.data or "{}"),

			"form_paypal": 	Form_Paypal(request),
			"form_check": 	Form_Check(request),
			"form_wire": 	Form_Wire(request),
			"form_direct": 	Form_Direct(request)
		})

	def post(self, request):
		success = False
		form = request.POST.get("form")

		# Validate choice
		if form == "PAYPAL":
			success = Form_Paypal(request).save()

		elif form == "CHECK":
			success = Form_Check(request).save()

		elif form == "WIRE":
			success = Form_Wire(request).save()

		elif form == "DIRECT":
			success = Form_Direct(request).save()

		# Success Message
		if success:
			messages.success(request, "Your billing information has been saved.")
		else:
			messages.error(request, "An error has occured. Your billing information has not been saved.")

		return self.get(request)