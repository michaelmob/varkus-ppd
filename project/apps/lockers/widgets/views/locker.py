from django.shortcuts import render, redirect
from ..models import Widget
from apps.leads.models import Token
from apps.offers.models import Offer
from django.core.validators import URLValidator

from ...files.views.locker import unlock as file_unlock
from ...links.views.locker import unlock as link_unlock
from ...lists.views.locker import unlock as list_unlock


def get_object(code):
	try:
		if not code:
			raise

		return Widget.objects.get(code=code)
	except:
		return None


def locker(request, code=None):
	obj = get_object(code)

	combo = Offer.get_locker_request_cache(request, obj, 15, 0.05)

	if not obj:
		return redirect("locker-404")

	return render(
		request,
		"offers/widget/external.html",
		{
			"obj": obj,
			"offers": combo.offers,
			"token": combo.token,
			"custom_css": obj.custom_css
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

	locker_obj = obj.locker_object()

	if locker_obj == None:
		url = obj.standalone_redirect

		validate = URLValidator()
		try:
			validate(url)
			return redirect(url)
		except:
			return redirect("widgets-complete")

	else:
		# You can only break this on the developers side
		unlock_method = eval(
			str(locker_obj.get_name().lower() + "_unlock")
				.replace(" ", "").replace(";", ""))

		return unlock_method(request, locker_obj.code, token)


def complete(request):
	return render(
		request,
		"offers/widget/complete.html", { }
	)