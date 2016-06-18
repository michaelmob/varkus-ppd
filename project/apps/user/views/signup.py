from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from ..models import Party
from datetime import datetime, date

from ..forms import Form_Sign_Up


class View_Sign_Up(View):
	def get(self, request, referrer=None):
		# User is logged in, redirect to dashboard
		if request.user.is_authenticated():
			return redirect("dashboard")

		return render(
			request, "user/signup.html",
			{
				"form": Form_Sign_Up,
				"invite_only": settings.INVITE_ONLY,
			}
		)

	def post(self, request):
		form = Form_Sign_Up(request.POST)
		user = form.create()

		if user and user.is_active:
			# Authenticate user, set to "user"
			user = authenticate(username=form.cleaned_data["username"],
				password=form.cleaned_data["password1"])

			# Log that user in
			login(request, user)

			messages.success(request, "Welcome to %s!" % settings.SITE_NAME)
			return redirect("dashboard")
		else:
			messages.success(request, "Welcome to %s! We'll notify you when your account is activated." % settings.SITE_NAME)
			return redirect("login")

		return render(
			request, "user/signup.html",
			{
				"form": form,
				"invite_only": settings.INVITE_ONLY,
			}
		)
