from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.urlresolvers import reverse

from ..forms import Link_Create, Link_Edit
from ..models import Link

from utils import charts
from utils import paginate, cache2


def display(request, page=1):
	if request.POST:
		return create(request)

	links = Link.objects.filter(user=request.user)
	links = paginate.pages(links, 15, page)

	return render(
		request,
		"lockers/links/display.html",
		{
			"links": links,
			"MAX_LINKS": settings.MAX_LINKS,
			"form": Link_Create()
		}
	)


def line_chart(request, code):
	try:
		obj = Link.objects.get(user=request.user, code=code)
	except Link.DoesNotExist:
		return JsonResponse({"data": None})

	return charts.line_chart_view(
		"charts__link_%s" % obj.pk,
		lambda: obj.earnings.get_leads()
	)


def delete(request, code=None):
	Link.objects.filter(user=request.user, code=code).delete()
	messages.success(request, "Your link has successfully been deleted.")
	return redirect("links")


def create(request):
	count = Link.objects.filter(user=request.user).count()

	if(count >= settings.MAX_LINKS):
		messages.error(request, "You have reached the link limit. Delete some to create a new one.")
		request.POST = None
		return display(request)

	form = Link_Create(request.POST)

	if not form.is_valid():
		messages.error(request, "There was an error creating your link. Please try again.")
		messages.error(request, form.errors)
		request.POST = None
		return display(request)

	obj = Link.create(
		user 		= request.user,
		name 		= form.cleaned_data["name"],
		description = form.cleaned_data["description"],
		url			= form.cleaned_data["url"],
	)

	return redirect("links-manage", obj.code)


def manage(request, code=None):
	if not code:
		return redirect("links")

	try:
		obj = Link.objects.get(user=request.user, code=code)
	except Link.DoesNotExist:
		return redirect("links")

	form = Link_Edit(
		request.POST or None,
		initial={
			"name": obj.name,
			"description": obj.description,
		}
	)

	# Save Link Edits
	if request.POST:
		if form.is_valid():
			obj.name = form.cleaned_data["name"]
			obj.description = form.cleaned_data["description"]
			obj.save()

	# Cache
	leads = cache2.get("leads__link_%s" % obj.pk, lambda: obj.earnings.get_leads(None))

	url = request.build_absolute_uri(reverse("links-locker", args=[obj.code]))

	return render(
		request,
		"lockers/links/manage/manage.html",
		{
			"data_url": reverse("links-manage-line-chart", args=[obj.code]),
			"form": form,
			"leads": leads,
			"obj": obj,
			"url": url
		}
	)
