from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse

from ..forms import Widget_Create, Widget_Edit
from ..models import Widget

from utils import charts as Charts
from utils import paginate, cache2


def display(request, page=1):
	if request.POST:
		return create(request)

	widgets = Widget.objects.filter(user=request.user)
	widgets = paginate.pages(widgets, 15, page)

	return render(
		request,
		"lockers/widgets/display.html",
		{
			"widgets": widgets,
			"MAX_WIDGETS": settings.MAX_WIDGETS,
			"form": Widget_Create()
		}
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
	chart = cache2.get("charts__widget_%s" % obj.pk, lambda: Charts.hour_chart(obj.earnings.get_leads()))

	url = request.build_absolute_uri(reverse("widgets-locker", args=[obj.code]))

	return render(
		request,
		"lockers/widgets/manage/manage.html",
		{
			"form": form,
			"leads": leads,
			"obj": obj,
			"chart": chart,
			"url": url
		}
	)
