from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.urlresolvers import reverse

from ..forms import Widget_Create, Widget_Edit
from ..models import Widget
from ..tables import Table_Widget

from utils import charts, cache2


def display(request, page=1):
	if request.POST:
		return create(request)

	table = Table_Widget.create(request)

	return render(
		request,
		"lockers/widgets/display.html",
		{
			"table": table,
			"MAX_WIDGETS": settings.MAX_WIDGETS,
			"form": Widget_Create()
		}
	)


def line_chart(request, code):
	try:
		obj = Widget.objects.get(user=request.user, code=code)
	except Widget.DoesNotExist:
		return JsonResponse({"data": None})

	return charts.line_chart_view(
		"charts__widget_%s" % obj.pk,
		lambda: obj.earnings.get_leads(),
		obj.earnings.get_clicks()
	)


def delete(request, code=None):
	Widget.objects.filter(user=request.user, code=code).delete()
	messages.success(request, "Your widget has been deleted.")
	return redirect("widgets")


def create(request):
	count = Widget.objects.filter(user=request.user).count()

	if(count >= settings.MAX_WIDGETS):
		messages.error(request, "You have reached the widget limit. Delete some to create a new one.")
		request.POST = None
		return display(request)

	form = Widget_Create(request.POST)

	if not form.is_valid():
		messages.error(request, "There was an error creating your widget. Please try again.")
		messages.error(request, form.errors)
		request.POST = None
		return display(request)

	obj = Widget.create(
		user 		= request.user,
		name 		= form.cleaned_data["name"],
		description = form.cleaned_data["description"]
	)

	return redirect("widgets-manage", obj.code)


""" Verify code and user owns object """
def verify(user, code):
	if not code:
		return None

	obj = None

	try:
		obj = Widget.objects.get(user=user, code=code)
		return obj
	except Widget.DoesNotExist:
		return None


def manage(request, code=None):
	obj = verify(request.user, code)

	if not obj:
		return redirect("widgets")

	form = Widget_Edit(
		request.POST or None,
		initial={
			"name": obj.name,
			"description": obj.description,
		}
	)

	# Save Widget Edits
	if request.POST:
		if form.is_valid():
			obj.name = form.cleaned_data["name"]
			obj.description = form.cleaned_data["description"]
			obj.save()

	# Cache
	leads = cache2.get("leads__widget_%s" % obj.pk, lambda: obj.earnings.get_leads(None))

	url = request.build_absolute_uri(reverse("widgets-locker", args=[obj.code]))

	return render(
		request,
		"lockers/widgets/manage/manage.html",
		{
			"data_url": reverse("widgets-manage-line-chart", args=[obj.code]),
			"form": form,
			"leads": leads,
			"obj": obj,
			"url": url
		}
	)
