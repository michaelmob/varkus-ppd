from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.core.validators import URLValidator
from ..forms import Form_Report


class View_Report(View):
	def get(self, request):
		url = request.GET.get("content")

		try:
			validate = URLValidator()
			validate(url)
		except:
			url = None

		return render(
			request, "support/report.html", {
				"content": url,
				"form": Form_Report(request)
			}
		)


	def post(self, request):
		obj = Form_Report(request).save()

		if obj:
			messages.success(request, "Your abuse report has been received. We'll investigate shortly. Thanks!")

		return redirect("report")