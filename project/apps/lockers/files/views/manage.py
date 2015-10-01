from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files import File as Django_File
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from ..models import File
from ..forms import File_Edit
from ..tables import Table_File

from utils import charts, cache2


def display(request, page=1):
	return render(
		request,
		"lockers/files/display.html",
		{
			"table": Table_File.create(request),
			"MAX_FILES": settings.MAX_FILES
		}
	)


def line_chart(request, code):
	try:
		obj = File.objects.get(user=request.user, code=code)
	except File.DoesNotExist:
		return JsonResponse({"data": None})

	return charts.line_chart_view(
		"charts__file_%s" % obj.pk,
		lambda: obj.earnings.get_leads(),
		obj.earnings.get_clicks(),
	)


def delete(request, code=None):
	File.objects.filter(user=request.user, code=code).delete()
	messages.success(request, "Your file has been deleted.")
	return redirect("files")


def upload(request):
	return render(
		request, "lockers/files/upload.html",
		{"MAX_UPLOAD_SIZE": settings.MAX_UPLOAD_SIZE}
	)


def manage(request, code=None):
	if not code:
		return redirect("files")

	try:
		obj = File.objects.get(user=request.user, code=code)
	except File.DoesNotExist:
		return redirect("files")

	form = File_Edit(
		request.POST or None,
		initial={
			"name": obj.name,
			"description": obj.description
		}
	)

	# Save List Edits
	if request.POST:
		if form.is_valid():
			obj.name = form.cleaned_data["name"]
			obj.description = form.cleaned_data["description"]
			obj.save()

	# Cache
	leads = cache2.get("leads__file_%s" % obj.pk, lambda: obj.earnings.get_leads(None))

	url = request.build_absolute_uri(reverse("files-locker", args=[obj.code]))

	return render(
		request,
		"lockers/files/manage/manage.html",
		{
			"data_url": reverse("files-manage-line-chart", args=[obj.code]),
			"form": form,
			"obj": obj,
			"leads": leads,
			"url": url
		}
	)


@require_POST
def process(request):
	try:
		success = False
		value = ""
		errors = 0

		count = File.objects.filter(user=request.user).count()

		if(count >= settings.MAX_FILES):
			return JsonResponse({
				"success": False,
				"value": "You have reached your maximum file limit."
			})

		disallowed_exts = [
			"exe", "bat", "com", "cmd", "vbs", "vbscript", "py",
		]

		# File Exists
		try:
			_file = Django_File(request.FILES["file"])
		except:
			value = "No file was delivered"
			errors += 1

		# File Type
		if errors < 1:
			ext = str(_file.name).lower().split('.')[-1]

			if(ext in disallowed_exts):
				value = "Disallowed file type"
				errors += 1

		# File Size
		if errors < 1:
			if(_file.size > settings.MAX_UPLOAD_SIZE):
				value = "File too large"
				errors += 1

		# Create File
		if errors < 1:
			obj = File.create(
				user=request.user,
				file=_file
			)

			success = True
			value = reverse("files-manage", args=[obj.code])

		return JsonResponse({
			"success": success,
			"value": value
		})
	except Exception as err:
		print(err)
