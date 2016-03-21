from django.shortcuts import render
from django.http import JsonResponse

from ...offers.models import Offer
from ..tables import Table_Offer
from ..bases.charts import Activity, Map


def index(request):
	offers 		= Offer.objects.order_by("-date")[:5]
	top_offers 	= Offer.objects.filter(payout__gt=0.75).order_by("-success_rate")[:5]

	return render(request, "cp/dashboard/dashboard.html", {
		"offers": Table_Offer.create(request, offers),
		"top_offers": Table_Offer.create(request, top_offers)
	})


def line_chart(request):
	return JsonResponse(Activity.output_cache(request.user))


def map_chart(request):
	return JsonResponse(Map.output_cache(request.user))
