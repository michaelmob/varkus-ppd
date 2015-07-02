from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.validators import URLValidator

from ..models import Widget
from .manage import verify
from ....lockers.utils import Locker_Item

from apps.lockers.files.models import File
from apps.lockers.links.models import Link
from apps.lockers.lists.models import List

def locker(request, code=None):
	obj = verify(request.user, code)
	if not obj:
		return redirect("widgets")

	if request.POST:
		locker_code = request.POST["locker"].lower().split(',')

		try:
			locker = locker_code[0]
			code = locker_code[1]
		except:
			locker = None
			code = None
			obj.standalone_redirect_url = request.POST.get("redirect", settings.SITE_URL).strip()
			obj.save()

		obj.set_locker(Locker_Item(locker, code, request.user))

		messages.success(request, "This widget's locker has been updated.")
		return redirect("widgets-manage", obj.code)

	files = File.objects.filter(user=request.user)
	links = Link.objects.filter(user=request.user)
	lists = List.objects.filter(user=request.user)

	return render(
		request,
		"lockers/widgets/manage/edit/locker.html",
		{
			"obj": obj,
			"files": files,
			"links": links,
			"lists": lists,
		}
	)


def postback(request, code=None):
	obj = verify(request.user, code)
	if not obj:
		return redirect("widgets")

	url = obj.postback_url

	if request.POST:
		url = request.POST.get("postback", "").strip()

		validate = URLValidator()
		try:
			validate(url)
			obj.postback_url = url
			obj.save()
			messages.success(request, "This widget's Postback URL has been updated.")
			return redirect("widgets-manage", obj.code)
		except:
			messages.error(request, "The Postback URL entered is invalid.")

	return render(
		request,
		"lockers/widgets/manage/edit/postback.html",
		{
			"obj": obj,
			"url": url,
		}
	)


def css(request, code=None):
	obj = verify(request.user, code)
	if not obj:
		return redirect("widgets")

	url = obj.custom_css_url

	if request.POST:
		url = request.POST.get("css", "").strip()

		if len(url) > 5:
			validate = URLValidator()
			try:
				validate(url)
				obj.custom_css_url = url
				obj.save()
				messages.success(request, "This widget's Custom CSS URL has been updated.")
				return redirect("widgets-manage", obj.code)
			except:
				messages.error(request, "The Custom CSS URL entered is invalid.")
		else:
			obj.custom_css_url = ""
			obj.save()

	return render(
		request,
		"lockers/widgets/manage/edit/css.html",
		{
			"obj": obj,
			"url": url,
		}
	)
