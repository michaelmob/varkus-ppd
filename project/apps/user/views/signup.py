from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from ..models import Party
from datetime import datetime, date

from ..forms import Form_Sign_Up


def signup(request, referrer=-1):
	# If logged in we don't need to be here
	if request.user.is_authenticated():
		return redirect("dashboard")

	form = Form_Sign_Up(request.POST or None, initial={"referrer": referrer})

	if request.POST:
		# If our form is valid we need to check that the
		# username and e-mail are not already in use
		# if both of them are unique we'll register this user
		if form.is_valid():
			username 	= form.cleaned_data["username"].strip()
			email 		= form.cleaned_data["email"].strip()
			password 	= form.cleaned_data["password"].strip()
			errors = 0

			if "@" in username:
				messages.error(request, "You cannot use an e-mail as your username.")
				errors += 1

			# Are we 18?
			try:
				birthday = datetime.strptime(
					"%s %s %s" % (
						form.cleaned_data["day"],
						form.cleaned_data["month"],
						form.cleaned_data["year"]
					),
					"%d %m %Y"
				)

				today = date.today()

				if(today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day)) < 18):
					# Not 18!
					messages.error(request, "You must be 18 years or older to use %s." % settings.SITE_NAME)
					errors += 1

			except:
				messages.error(request, "We know that's not your real birthday!")
				errors += 1

			# Username is already taken
			if User.objects.filter(username__iexact=username).count() > 0:
				messages.error(request, "The username \"%s\" is already in use." % username)
				errors += 1

			# E-mail is already taken
			if User.objects.filter(email__iexact=email).count() > 0:
				messages.error(request, "The e-mail \"%s\" is already in use." % email)
				errors += 1

			# No errors! Let's create the account
			if errors < 1:
				user = User.objects.create_user(username, email, password)
				user.is_active = not settings.INVITE_ONLY
				user.first_name = form.cleaned_data["first_name"].strip()
				user.last_name = form.cleaned_data["last_name"].strip()

				# DEBUG:
				# Create Superuser if doesn't exist
				if settings.DEBUG:
					if User.objects.filter(is_superuser=True).count() < 1:
						user.is_staff = True
						user.is_superuser = True

				user.save()

				# If referrer exists
				try:
					referrer = int(form.cleaned_data["referrer"].strip())

					if referrer > 0:
						user.profile.referrer = User.objects.get(pk=referrer)
				except:
					pass

				user.profile.party = Party.default()
				user.profile.birthday = birthday
				user.profile.save()

				if user.is_active:
					user = authenticate(username=username, password=password)
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