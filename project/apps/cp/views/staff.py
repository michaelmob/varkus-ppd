import psutil, platform

from datetime import timedelta

from django.shortcuts import render, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache

from ...leads.models import Deposit


@user_passes_test(lambda u: u.is_superuser)
def server(request):
	data = cache.get("system_data")
	
	#if not data:
	with open('/proc/uptime', 'r') as f:
		uptime = str(timedelta(seconds=float(f.readline().split()[0]))).split('.')[0]
		
	memory = psutil.virtual_memory()

	data = {
		"cpu": psutil.cpu_percent(interval=0.1),
		"cpu_count": psutil.cpu_count(),
		"memory_total": memory.total,
		"memory_used": memory.total - memory.available,
		"swap": psutil.swap_memory(),
		"disk": psutil.disk_usage('/'),
		"uptime": uptime,
		"uname": platform.uname(),
	}

	cache.set("system_data", data, 60)

	return render(request, "cp/staff/server.html", data)


@staff_member_required
def info(request):
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
