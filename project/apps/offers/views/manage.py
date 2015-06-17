from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.db.models import Q
from ..models import Offer
from ..forms import Form_Offer
from utils import paginate

from utils import charts as Charts

orders = {
	"name": "name",
	"cat": "category",
	"ctry": "country",
	"ua": "user_agent",
	"epc": "earnings_per_click",
	"pay": "payout",
}


def list(request, page=1, column="epc", order="desc"):
	try:
		order_ = ("-" if order == "desc" else "") + orders[column]
	except KeyError:
		column = "epc"
		order_ = "-earnings_per_click"

	query = request.GET.get("q")

	if query:
		offers = Offer.objects.filter(
			Q(name__icontains=query) | Q(anchor__icontains=query)
		).order_by(order_)
	else:
		offers = Offer.objects.all().order_by(order_)

	# Pagination
	offers = paginate.pages(offers, 30, page)

	return render(
		request, "offers/list.html",
		{
			"offers": offers,
			"column": column,
			"order": order,
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

	# Cache Offer Leads
	key = "charts__offer_%s" % id
	chart = cache.get(key)

	if (not chart):
		leads = offer.earnings.get_leads()
		chart = Charts.hour_chart_lead_count(leads)
		cache.set(key, chart, 3600)

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
			"offer": offer,
			"hour_chart": chart,
			"form": form
		}
	)


def priority(request):
	id = request.GET.get("remove", None)

	if(id):
		request.user.profile.offer_block.remove(id)
		request.user.profile.offer_priority.remove(id)

	return render(request, "offers/priority.html", {})
