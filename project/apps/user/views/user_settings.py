from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import Form_Personal_Details, Form_Account_Details


def user_settings(request, save=None):
	form_personal = Form_Personal_Details(
		request.POST or None,
		initial={
			"first_name": request.user.first_name,
			"last_name": request.user.last_name,
			"country": request.user.profile.country,
			"website": request.user.profile.website
		}
	)

	form_account = Form_Account_Details(
		request.POST or None,
		initial={
			"email": request.user.email,
		}
	)

	if request.POST:
		if save == "personal" and form_personal.is_valid():
			request.user.first_name 		= form_personal.cleaned_data["first_name"]
			request.user.last_name 			= form_personal.cleaned_data["last_name"]
			request.user.profile.country 	= form_personal.cleaned_data["country"]
			request.user.profile.website	= form_personal.cleaned_data["website"]

			request.user.save()
			request.user.profile.save()

		elif save == "account" and form_account.is_valid():
			request.user.email 				= form_account.cleaned_data["email"]

	full_url = request.build_absolute_uri().split('/')[:3]

	return render(request, "user/settings/settings.html",
		{
			"full_url": "/".join(full_url),
			"form_personal": form_personal,
			"form_account": form_account
		}
	)