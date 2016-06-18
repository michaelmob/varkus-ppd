from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from ..tables import Table_Referrals
from ..forms import Form_Personal_Details, Form_Account_Details


class View_Settings(View):
	def get(self, request):
		referral_amount = int(request.user.profile.party.referral_cut_amount * 100)

		return render(
			request, "user/account/settings.html", {
				"url": request.build_absolute_uri(reverse("signup-referral", args=(request.user.id,))),
				"percent": referral_amount,
				"referrals": Table_Referrals(request),

				"form_account": Form_Account_Details(request),
				"form_personal": Form_Personal_Details(request),
			}
		)

	def post(self, request):
		form = request.POST.get("form")

		if form == "ACCOUNT" and Form_Account_Details(request).save():
			messages.success(request, "Your account details have been updated.")

		elif form == "PERSONAL" and Form_Personal_Details(request).save():
			messages.success(request, "Your personal details have been updated.")

		else:
			messages.error(request, "An error has occured.")

		return self.get(request)