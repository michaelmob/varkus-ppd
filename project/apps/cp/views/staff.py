import os, psutil, platform

from datetime import timedelta
from random import randint

from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.contrib import messages
from django.conf import settings

from apps.lockers.widgets.models import Widget
from apps.offers.models import Offer
from apps.conversions.models import Conversion, Token

@method_decorator(staff_member_required, name="dispatch")
class Server(View):
	def dispatch(self, *args, **kwargs):
		if self.request.is_ajax():
			return self.ajax(self.request, **kwargs)

		return super(__class__, self).dispatch(*args, **kwargs)

	def ajax(self, request, action):
		# Clear Offer Cache
		if action == "clear-cache":
			cache.clear()
			return JsonResponse({
				"success": True,
				"message": "Offer cache has been cleared."
			})

		# Create Token or Conversion randomly
		if action == "create-conversion":
			button_text = "Denied"
			created = False

			if settings.DEBUG:
				widget = Widget.objects.filter(user=request.user, name="TEST").first()

				if widget:
					for n in range(randint(0, 15)):
						Token.random(widget)

					conversion = Conversion.get_or_create(
						Token.random(widget), datetime="TOKEN")

					if conversion:
						created = True
						button_text = "Created"
				else:
					button_text = "Denied; Create a widget named \"TEST\""

			return JsonResponse({
				"success": True,
				"data": {"text": button_text}
			})


	def get(self, request, action=None):
		with open("/proc/uptime", 'r') as f:
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
			"uname": platform.uname() }

		return render(request, "cp/staff/server.html", data)

	def post(self, request):
		if (request.POST.get("password") != os.environ.get("ADVANCED_PASSWORD", "CheeseDoodles")) \
			or (int(request.session.get("advanced_attempts", 0)) > 2):

			# Anti-Bruteforce
			request.session["advanced_attempts"] = \
				request.session.get("advanced_attempts", 0) + 1

			messages.error(request, "Not quite right! (%s attempts)" % request.session["advanced_attempts"])
			return self.get(request)

		request.session["advanced_superuser"] = True
		return redirect("staff-advanced")


@method_decorator(staff_member_required, name="dispatch")
class Advanced(View):
	def get(self, request):
		if not request.session.get("advanced_superuser"):
			return redirect("staff-server")

		return render(request, "cp/staff/advanced.html")