from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..forms import Form_Report
from ..models import Abuse_Report
from django.conf import settings
from utils import files, strings


def page(request):
	# Set default initials if user is logged in
	if request.user.is_authenticated():
		form = Form_Report(initial={
			"name": "%s %s" % (request.user.first_name, request.user.last_name),
			"email": request.user.email
		})
	else:
		form = Form_Report()

	if request.POST:
		form = action(request)

	return render(
		request,
		"support/report.html",
		{
			"form": form,
			"complaints": Abuse_Report.COMPLAINTS
		}
	)


def action(request):
	form = Form_Report(request.POST)

	if not form.is_valid():
		if len(form["captcha"].errors) > 0:
			messages.error(request, "Your captcha was incorrect!")
		else:
			messages.error(request, "Something went wrong! Please try again.")
			
		return form

	# Add the 3 files, so we don't get a
	# malicious user who is trying to upload more/bigger files
	images = []

	for file in request.FILES:
		image = request.FILES[file]

		if len(image) > settings.REPORT_MAX_FILE_SIZE:
			messages.error(request, "Files may not be larger than 4 megabytes.")
			return form

		if not files.check_image(image):
				messages.error(request, "Uploaded files must be images.")
				return form

		images.append(image)

	# Just add None, so we dont run into list index out of range
	for i in range(3):
		images.append(None)

	# Create our object and take her home!
	report = Abuse_Report.objects.create(
		name=form.cleaned_data["name"],
		email=form.cleaned_data["email"],
		user=request.user if request.user.is_authenticated() else None,
		ip_address=request.META.get("REMOTE_ADDR"),
		date_time=datetime.now(),
		complaint=form.cleaned_data["complaint"],
		text=form.cleaned_data["text"],
	)

	# Now upload each of our files as (id)-(#).ext
	for i in range(len(images)):
		if images[i]:
			images[i] = default_storage.save(
				# tickets/2014/11/15/19-(strlen32).jpg
				"reports/%s/%s/%s" % (
					datetime.now().strftime("%Y/%m"),  # Year/Month
					report.pk,  # Report ID
					"%s-%s.%s" % (
						# 15-(strlen32).jpg
						i + 1,
						strings.random(32),
						images[i].name.split(".")[-1]
					)
				),
				images[i]
			)

	# Add the images to our report and save
	report.image1 = images[0]
	report.image2 = images[1]
	report.image3 = images[2]
	report.save()

	messages.success(request, "Your abuse report has been received. We'll investigate shortly. Thanks!")
	
	return Form_Report()