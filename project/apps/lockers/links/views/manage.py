from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse

from ..forms import Link_Create, Link_Edit
from ..models import Link

from utils import charts as Charts
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
		item = Link.objects.get(user=request.user, code=code)
	except Link.DoesNotExist:
		return redirect("links")

	form = Link_Edit(
		request.POST or None,
		initial={
			"name": item.name,
			"description": item.description,
		}
	)

	# Save Link Edits
	if request.POST:
		if form.is_valid():
			item.name = form.cleaned_data["name"]
			item.description = form.cleaned_data["description"]
			item.save()

	# Cache
	leads = cache2.get("leads__link_%s" % item.pk, lambda: item.earnings.get_leads(None))
	chart = cache2.get("charts__link_%s" % item.pk, lambda: Charts.hour_chart(item.earnings.get_leads()))

	url = request.build_absolute_uri(reverse("links-locker", args=[item.code]))

	return render(
		request,
		"lockers/links/manage/manage.html",
		{
			"form": form,
			"leads": leads,
			"item": item,
			"chart": chart,
			"url": url
		}
	)
