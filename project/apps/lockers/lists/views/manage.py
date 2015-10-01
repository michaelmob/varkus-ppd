from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.urlresolvers import reverse

from ..forms import List, List_Create, List_Edit
from ..tables import Table_List

from utils import charts, cache2


def display(request, page=1):
	if request.POST:
		return create(request)

	return render(
		request,
		"lockers/lists/display.html",
		{
			"table": Table_List.create(request),
			"MAX_LISTS": settings.MAX_LISTS,
			"form": List_Create()
		}
	)


def line_chart(request, code):
	try:
		obj = List.objects.get(user=request.user, code=code)
	except List.DoesNotExist:
		return JsonResponse({"data": None})

	return charts.line_chart_view(
		"charts__list_%s" % obj.pk,
		lambda: obj.earnings.get_leads(),
		obj.earnings.get_clicks()
	)


def delete(request, code=None):
	List.objects.filter(user=request.user, code=code).delete()
	messages.success(request, "Your list has successfully been deleted.")
	return redirect("lists")


def create(request):

	count = List.objects.filter(user=request.user).count()

	if(count >= settings.MAX_LISTS):
		messages.error(request, "You have reached the List limit. Delete some to create a new one.")
		request.POST = None
		return display(request)

	form = List_Create(request.POST)

	if not form.is_valid():
		messages.error(request, "There was an error creating your list. Please try again.")
		messages.error(request, form.errors)
		request.POST = None
		return display(request)

	obj = List.create(
		user 		= request.user,
		description = form.cleaned_data["description"],
		name 		= form.cleaned_data["name"],
		item_name	= form.cleaned_data["item_name"],
		items 		= form.cleaned_data["items"],
		order 		= form.cleaned_data["order"],
		delimeter 	= form.cleaned_data["delimeter"],
		reuse 		= form.cleaned_data["reuse"],
	)

	return redirect("lists-manage", obj.code)


def manage(request, code=None):
	if not code:
		return redirect("lists")

	try:
		obj = List.objects.get(user=request.user, code=code)
	except List.DoesNotExist:
		return redirect("lists")

	form = List_Edit(
		request.POST or None,
		initial={
			"name": obj.name,
			"description": obj.description,
			"order": obj.order,
			"reuse": obj.reuse,
			"item_name": obj.item_name
		}
	)

	# Save List Edits
	if request.POST:
		if form.is_valid():
			obj.name = form.cleaned_data["name"]
			obj.description = form.cleaned_data["description"]
			obj.order	= form.cleaned_data["order"]
			obj.reuse = form.cleaned_data["reuse"]
			obj.item_name = form.cleaned_data["item_name"]
			obj.save()

	# Cache
	leads = cache2.get("leads__list_%s" % obj.pk, lambda: obj.earnings.get_leads(None))

	url = request.build_absolute_uri(reverse("lists-locker", args=[obj.code]))

	return render(
		request,
		"lockers/lists/manage/manage.html",
		{
			"data_url": reverse("lists-manage-line-chart", args=[obj.code]),
			"form": form,
			"leads": leads,
			"obj": obj,
			"url": url
		}
	)
