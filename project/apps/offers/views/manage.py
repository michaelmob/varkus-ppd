from urllib.parse import unquote

from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q

from ..models import Offer
from ..forms import Form_Offer

from utils import paginate
from utils import charts

offer_list_columns = [
	"name", "category", "flag", "user_agent",
	"earnings_per_click", "payout"
]


def list(request, page=1):

	# Multi-Sort Table
	query = request.GET.get("q")
	sort = request.GET.get("o", "").split(',')
	order = ["-date"]

	if sort[0] != "":
		for idx in sort:
			try:
				idx = int(idx)
				order.append(
					("-" if idx < 0 else "") +
					offer_list_columns[abs(idx) - 1]
				)
			except:
				pass

	get_params = request.GET.urlencode().replace("%2C", ",")

	if query:
		offers = Offer.objects.filter(earnings_per_click__gt="0.01").filter(
			Q(name__icontains=query) | Q(anchor__icontains=query)
		).order_by(*order)
	else:
		offers = Offer.objects.all().filter(earnings_per_click__gt="0.01").order_by(*order)

	# Pagination
	offers = paginate.pages(offers, 30, page)

	return render(
		request, "offers/list.html",
		{
			"get_params": get_params,
			"offers": offers,
			"query": query
		}
	)


def offer(request, id=None):
	if not id:
		return redirect("offers")

	try:
		offer = Offer.objects.get(id=id)
	except Offer.DoesNotExist:
		return redirect("offers")

	# Get initial
	if offer in request.user.profile.offer_block.all():
		priority = "1"
	elif offer in request.user.profile.offer_priority.all():
		priority = "2"
	else:
		priority = "0"

	form = Form_Offer(request.POST or None, initial={"priority": priority})

	# Set Priority
	if request.POST:
		if form.is_valid():
			priority = form.cleaned_data["priority"]

			request.user.profile.offer_block.remove(offer)
			request.user.profile.offer_priority.remove(offer)

			if priority == "1":
				request.user.profile.offer_block.add(offer)
				messages.success(request, "This offer has been blocked from your lockers.")
			elif priority == "2":
				request.user.profile.offer_priority.add(offer)
				messages.success(request, "This offer has been prioritized in your lockers.")
			else:
				messages.info(request, "This offer has been set to neutral.")

	return render(
		request, "offers/manage.html",
		{
			"data_url": reverse("offers-manage-line-chart", args=[offer.pk]),
			"offer": offer,
			"form": form
		}
	)


def line_chart(request, id=None):
	try:
		obj = Offer.objects.get(id=id)
	except Offer.DoesNotExist:
		return JsonResponse({"data": None})

	return charts.line_chart_view(
		"charts__offer_%s" % obj.pk,
		lambda: obj.earnings.get_leads(),
		obj.earnings.get_clicks(),
		no_earnings=True
	)


def priority(request):
	id = request.GET.get("remove", None)

	if(id):
		request.user.profile.offer_block.remove(id)
		request.user.profile.offer_priority.remove(id)

	return render(request, "offers/priority.html", {})
