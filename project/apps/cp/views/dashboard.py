from django.shortcuts import render
from django.http import JsonResponse

from apps.conversions.models import Conversion
from apps.offers.models import Offer
from ..tables import Table_Offer, Table_Conversions
from ..models import Notification
from ..bases.charts import Activity, Map


def index(request):
	return render(request, "cp/dashboard/dashboard.html", {
		"offers": Table_Offer(request, Offer.objects.order_by("-date")[:5]),

		"top_offers": Table_Offer(request,Offer.objects.filter(
			payout__gt=0.75).order_by("-success_rate")[:5]),

		"conversions": Table_Conversions(request, Conversion.objects.filter(
			user=request.user).order_by("-datetime")[:5])
	})


def line_chart(request):
	return JsonResponse(Activity.output_cache(request.user))


def map_chart(request):
	return JsonResponse(Map.output_cache(request.user))


def notifications(request, action=None):
	if action == "read":
		Notification.mark_read(request.user)

		return JsonResponse({
			"success": True,
			"message": "Notifications have been marked as read.",
			"data": []
		})

	return render(request, "cp/dashboard/notifications.html")