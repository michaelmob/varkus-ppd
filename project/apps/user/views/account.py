from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from ..tables import Table_Referrals
from ..forms import Form_Personal_Details, Form_Account_Details


class View_Settings(View):
	def get(self, request):
		# Get Referral Amount
		try:
			referral_amount = int((request.user.profile.party.referral_cut_amount or .1) * 100)
		except:
			referral_amount = 10
			request.user.profile.party.referral_cut_amount = 0.10
			request.user.profile.party.save()

		return render(
			request, "user/account/settings.html", {
				"url": request.build_absolute_uri(reverse("signup-referral", args=(request.user.id,))),
				"percent": referral_amount,
				"referrals": Table_Referrals.create(request),
				"form_account": Form_Account_Details.create(request),
				"form_personal": Form_Personal_Details.create(request),
			}
		)

	def post(self, request):
		section = request.POST.get("section")

		if section == "account":
			form = Form_Account_Details.create(request).save()

		elif section == "personal":
			form = Form_Personal_Details.create(request).save()

		return self.get(request)