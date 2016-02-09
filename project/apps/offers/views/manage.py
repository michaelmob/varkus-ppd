from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from apps.leads.models import Lead

from ..models import Offer
from ..forms import Form_Offer
from ..tables import Table_Offer_All, Table_Offer_Leads, Table_Offer_Options

from apps.cp.bases.charts import Charts


class View_Overview(View):
	def get(self, request):
		query = request.GET.get("query", None)

		if query:
			offers = Offer.objects.filter(earnings_per_click__gt=0.01) \
				.filter(Q(name__icontains=query) | Q(anchor__icontains=query))
		else:
			offers = Offer.objects.filter(earnings_per_click__gt=0.01)

		return render(request, "offers/overview.html", {
			"query": query,
			"offers": Table_Offer_All.create(request, offers)
		})


class View_Manage(View):
	def get(self, request, id):
		# Get offer if exists, or redirect to Offers page
		try:
			int(id)
			obj = Offer.objects.get(id=id)
		except (ValueError, Offer.DoesNotExist):
			return redirect("offers")

		leads = Lead.objects.filter(offer=obj, user=request.user).order_by("-date_time")

		# Set offer importance
		importance = "neutral"

		if obj in request.user.profile.offer_block.all():
			importance = "block"
		elif obj in request.user.profile.offer_priority.all():
			importance = "priority"

		return render(request, "offers/manage.html", {
			"obj": obj,
			"leads": Table_Offer_Leads.create(request, leads),
			"importance": importance
		})


class View_Options(View):
	def get(self, request):
		return render(request, "offers/options.html", {
			"prioritized": Table_Offer_Options.create(
				request, request.user.profile.offer_priority.all()),

			"blocked": Table_Offer_Options.create(
				request, request.user.profile.offer_block.all())
		})


class View_Importance(View):
	def get(self, request, id, importance):
		result = {
			"success": True,
			"message": "Offer importance has been set to neutral.",
			"data": {
				"importance": "neutral"
			}
		}

		try:
			int(id)
			obj = Offer.objects.get(id=id)
		except (ValueError, Offer.DoesNotExist):
			result["success"] = False
			result["message"] = "Offer does not exist."

		# Remove Offer
		request.user.profile.offer_block.remove(id)
		request.user.profile.offer_priority.remove(id)

		# Priority
		if importance == "priority":
			request.user.profile.offer_priority.add(obj)
			result["message"] = "Offer importance has been set to priority."
			result["data"]["importance"] = "priority"

		# Block
		elif importance == "block":
			request.user.profile.offer_block.add(obj)
			result["message"] = "Offer importance has been set to blocked."
			result["data"]["importance"] = "block"

		return JsonResponse(result)


class View_Line_Chart(View):
	def get(self, request, id):
		# Get offer if exists, or return None
		try:
			int(id)
			obj = Offer.objects.get(id=id)
		except (ValueError, Offer.DoesNotExist):
			return JsonResponse({"data": None})

		return JsonResponse(Charts.line_cache(obj))
