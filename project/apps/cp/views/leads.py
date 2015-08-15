from django.shortcuts import render, HttpResponse
from django.core.cache import cache
from ...leads.models import Lead

from utils import cache2


def index(request):
	return render(request, "cp/leads/index.html", {})


def poll(request):
	return HttpResponse(request.user.earnings.leads)
