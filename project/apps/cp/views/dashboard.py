import psutil
import platform

from datetime import timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.admin.views.decorators import staff_member_required

from ...leads.models import Lead, Deposit
from ...offers.models import Offer

from ..tables import Table_Offer, Table_Lead
from ..bases.charts import Charts


def index(request):
	offers = Offer.objects.order_by('-date')[:5]
	leads = Lead.objects.filter(lead_blocked=False, user=request.user).order_by("-date_time")[:5]

	return render(request, "cp/dashboard/index.html", {
		"offers": offers,
		"offers_table": Table_Offer.create(request, offers),
		"leads_table": Table_Lead.create(request, leads)
	})


def line_chart(request):
	return JsonResponse(Charts.line_cache(request.user))


def map_chart(request):
	return JsonResponse(Charts.map_cache(request.user))


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
