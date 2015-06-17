from django.shortcuts import render, redirect, HttpResponse
from ..models import File
from ....leads.models import Token
from ....offers.models import Offer


def get_object(code):
	try:
		if not code:
			raise

		return File.objects.get(code=code)
	except:
		return None


def locker(request, code=None):
	obj = get_object(code)

	combo = Offer.get_locker_request_cache(request, obj, 15, 0.05)

	if not obj:
		return redirect("locker-404")

	return render(
		request,
		"lockers/files/locker.html",
		{
			"item": obj,
			"offers": combo.offers,
			"token": combo.token
		}
	)


def unlock(request, code=None):
	obj = get_object(code)

	if not obj:
		return redirect("locker-404")

	token = Token.get_or_create_request(request, obj)

	# Give access
	if not token.access():
		return redirect("home")

	return render(
		request,
		"lockers/files/unlock.html",
		{
			"item": obj,
			"data": token.data
		}
	)


def download(request, code=None):
	obj = get_object(code)

	if not obj:
		return redirect("locker-404")

	token = Token.get_or_create_request(request, obj)

	# Give access
	if not token.access():
		return redirect("home")

	# Download
	response = HttpResponse(obj.file, content_type="application/octet-stream")
	response["Content-Disposition"] = "attachment; filename=\"%s\"" % obj.file_name

	return response
