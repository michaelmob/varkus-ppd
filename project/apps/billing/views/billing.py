from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic.edit import FormView
from .. import forms
from ..models import Invoice, Billing
from ..tables import InvoiceTable



class BillingUpdateView(SuccessMessageMixin, FormView):
	"""
	View to update a User's billing profile.
	"""
	template_name = "billing/billing_update.html"
	success_url = reverse_lazy("billing:list")
	success_message = "Your billing details have been updated."


	def get_form_class(self):
		"""
		Return form class to be used based on 'form' post value.
		"""
		form = self.request.POST.get("form")

		if not form or form == "PAYPAL":
			self.form_class = forms.PaypalForm

		elif form == "CHECK":
			self.form_class = forms.CheckForm

		elif form == "WIRE":
			self.form_class = forms.WireForm

		elif form == "DIRECT":
			self.form_class = forms.DirectDepositForm

		return self.form_class


	def get_context_data(self, *args, **kwargs):
		"""
		Modify context dictionary to add all forms.
		"""
		context = super(__class__, self).get_context_data(*args, **kwargs)
		post_data = self.request.POST or None
		billing_data = self.request.user.billing.get_data()

		context["form"] = {
			"paypal": forms.PaypalForm(
				post_data, initial=billing_data.get("PAYPAL")
			),

			"check": forms.CheckForm(
				post_data, initial=billing_data.get("CHECK")
			),

			"wire": forms.WireForm(
				post_data, initial=billing_data.get("WIRE")
			),

			"direct": forms.DirectDepositForm(
				post_data, initial=billing_data.get("DIRECT")
			)
		}

		context["active_tab"] = self.request.POST.get("form")

		return context


	def form_valid(self, form):
		"""
		Save billing profile from forms.
		"""
		form.save_user(self.request.user)
		return super(__class__, self).form_valid(form)