from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.admin.views.decorators import staff_member_required
from ...leads.models import Lead
from ...offers.models import Offer

from utils import charts
from utils import cache2


def index(request):
	# Cache Newest Offers and Recent Leads
	offers = cache2.get("newest_offers", lambda: Offer.objects.order_by('-date')[:5])
	leads = cache2.get("recent__user_%s" % request.user.id, lambda: Lead.objects.filter(lead_blocked=False, user=request.user).order_by("-date_time")[:5])

	return render(request, "cp/dashboard/index.html", {
		"offers": offers,
		"leads": leads,
	})


def line_chart(request):
	return charts.line_chart_view(
		"charts_line__user_%s" % request.user.id,
		lambda: request.user.earnings.get_leads(),
		request.user.earnings.get_clicks()
	)


def map_chart(request):
	return charts.map_chart_view(
		"charts_map__user_%s" % request.user.id,
		lambda: request.user.earnings.get_leads()
	)


@staff_member_required
def staff(request):
	return render(request, "cp/dashboard/staff.html", {})


@staff_member_required
def staff_info(request):
	output = "<h1>META</h1>"
	for k, v in request.META.items():
		output += "<strong>%s</strong>: %s<br/>" % (k, v,)

	output += "<br/><br/><h1>POST</h1>"
	for k, v in request.POST.items():
		output += "<strong>%s</strong>: %s<br/>" % (k, v,)

	output += "<br/><br/><h1>GET</h1>"
	for k, v in request.GET.items():
		output += "<strong>%s</strong>: %s<br/>" % (k, v,)

	return HttpResponse(output)
