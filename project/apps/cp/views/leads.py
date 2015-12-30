from django.shortcuts import render, HttpResponse
from django.core.cache import cache
from ...leads.models import Lead


def index(request):
	if request.user.profile.notification_lead > 0:
		request.user.profile.notification_lead = 0
		request.user.profile.save()

	return render(request, "cp/leads/index.html", {})


def poll(request):
	return HttpResponse(request.user.earnings.leads)
