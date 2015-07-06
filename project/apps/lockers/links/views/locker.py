from django.shortcuts import render, redirect
from django.conf import settings
from ..models import Link
from ....leads.models import Token
from ....offers.models import Offer


def get_object(code):
	try:
		if not code:
			raise

		return Link.objects.get(code=code)
	except:
		return None


def locker(request, code=None):
	obj = get_object(code)

	if not obj:
		return redirect("locker-404")

	combo = Offer.get_locker_request_cache(request, obj, settings.OFFERS_COUNT, 0.05)

	return render(
		request,
		"lockers/links/locker.html",
		{
			"obj": obj,
			"offers": combo.offers,
			"token": combo.token
		}
	)


def unlock(request, code=None, token=None):
	obj = get_object(code)

	if not obj:
		return redirect("locker-404")

	if not token:
		token = Token.get_or_create_request(request, obj)

	# Give access
	if not token.access():
		return redirect("home")

	return render(
		request,
		"lockers/links/unlock.html",
		{
			"obj": obj,
			"data": obj.url
		}
	)
