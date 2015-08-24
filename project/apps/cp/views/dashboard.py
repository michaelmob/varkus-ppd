import psutil
import platform

from datetime import timedelta

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.admin.views.decorators import staff_member_required

from ...leads.models import Lead, Deposit
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
	data = cache.get("system_data")
	
	if not data:
		with open('/proc/uptime', 'r') as f:
			uptime = str(timedelta(seconds=float(f.readline().split()[0]))).split('.')[0]
			
		data = {
			"cpu": psutil.cpu_percent(interval=0.1),
			"cpu_count": psutil.cpu_count(),
			"memory": psutil.virtual_memory(),
			"swap": psutil.swap_memory(),
			"disk": psutil.disk_usage('/'),
			"uptime": uptime,
			"uname": platform.uname(),
		}

		cache.set("system_data", data, 60)

	return render(request, "cp/dashboard/staff.html",
		{
			"data": data,
			"deposits": Deposit.objects.all()
		}
	)


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
