from django.shortcuts import render, redirect
from ..models import List
from ....leads.models import Token
from ....offers.models import Offer


def get_object(code):
	try:
		if not code:
			raise

		return List.objects.get(code=code)
	except:
		return None


def locker(request, code=None):
	obj = get_object(code)

	combo = Offer.get_locker_request_cache(request, obj, 15, 0.05)

	if not obj:
		return redirect("locker-404")

	return render(
		request,
		"lockers/lists/locker.html",
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

	if not token.data:
		token.data = obj.get()
		token.save()

	return render(
		request,
		"lockers/lists/unlock.html",
		{
			"obj": obj,
			"data": token.data
		}
	)
