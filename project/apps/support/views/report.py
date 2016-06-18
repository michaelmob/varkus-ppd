from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from ..forms import Form_Report
from ..models import Abuse_Report


class View_Report(View):
	def get(self, request):
		return render(
			request, "support/report.html", {
				"form": Form_Report(request)
			}
		)

	def post(self, request):
		obj = Form_Report(request).save()

		if obj:
			messages.success(request, "Your abuse report has been received. We'll investigate shortly. Thanks!")

		return redirect("report")