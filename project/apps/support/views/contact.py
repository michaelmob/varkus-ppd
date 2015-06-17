from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from apps.support.forms import Form_Contact
from apps.support.models import Contact_Message


def page(request):
	# Set default initials if user is logged in
	if request.user.is_authenticated():
		form = Form_Contact(initial={
			"name": "%s %s" % (request.user.first_name, request.user.last_name),
			"email": request.user.email
		})
	else:
		form = Form_Contact()

	if request.POST:
		form = action(request)

	return render(
		request,
		"support/contact.html",
		{
			"form": form
		}
	)


def action(request):
	form = Form_Contact(request.POST)

	# Django-Captcha either has an error with Python 3.4 or Django 1.7
	# so wrapping it in a try except tells us if the captcha is incorrect
	# once it's fixed, we'll remove this
	try:
		if not form.is_valid():

			# Captcha field has errors
			if len(form["captcha"].value()[1]) < 1:
				messages.error(request, "You have forgotten to enter a CAPTCHA!")
			else:
				messages.error(request, "You have entered an incorrect CAPTCHA.")

			return form
	except AttributeError:
		messages.error(request, "You have entered an incorrect CAPTCHA.")
		return form

	# No errors, so let's add it to our message collection
	messages.success(request, "Your message has been received. Thanks for your feedback!")

	Contact_Message.objects.create(
		name=form.cleaned_data["name"],
		email=form.cleaned_data["email"],
		user=request.user if request.user.is_authenticated() else None,
		ip_address=request.META.get("REMOTE_ADDR"),
		date_time=datetime.now(),
		subject=form.cleaned_data["subject"],
		message=form.cleaned_data["message"],
	)

	return Form_Contact()