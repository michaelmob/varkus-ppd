from django.views.generic import View
from django.shortcuts import render

from ..forms import Form_Conversions_Range
from ..tables import Table_Conversions

class View_Conversions(View):
	page = "month"
	title = "Conversions"
	table = Table_Conversions
	table_icon = "lightning"
	template = "conversions/overview.html"

	def get(self, request):
		form = Form_Conversions_Range.from_request(request)
		table = self.table(request, form.date_range())
		date_range = "custom" if request.GET.get("f") else request.GET.get("r", "month")

		return render(request, self.template, {
			"page": self.page,
			"title": self.title,
			"form": form,
			"table": table,
			"date_range": date_range,
			"table_icon": self.table_icon
		})
