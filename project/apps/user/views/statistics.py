from datetime import date, timedelta

from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from ..forms import Form_Statistics
from ..tables import Table_Statistics_Offers, Table_Statistics_Countries

class View_Statistics(View):
	page = "month"
	title = "Statistics"
	table = None

	def get(self, request):
		form = Form_Statistics.create(request.GET)
		table = self.table(request, form.date_range())
		date_range = "custom" if request.GET.get("f") else request.GET.get("r")

		return render(
			request, "user/statistics/statistic.html", {
				"page": self.page,
				"title": self.title,
				"form": form,
				"table": table,
				"date_range": date_range
			}
		)


class View_Offers(View_Statistics):
	page = "offers"
	title = "Offer Statistics"
	table = Table_Statistics_Offers


class View_Countries(View_Statistics):
	page = "countries"
	title = "Country Statistics"
	table = Table_Statistics_Countries


class View_Chargebacks(View_Statistics):
	page = "chargebacks"
	title = "Chargeback Statistics"