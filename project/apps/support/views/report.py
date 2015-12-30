from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from ..forms import Form_Report
from ..models import Abuse_Report


class View_Report(View):
	def get(self, request):
		return render(
			request, "support/report.html", {
				"form": Form_Report(
					initial = {
						"name": "%s %s" % (
							request.user.first_name,
							request.user.last_name
						),
						"email": request.user.email
					} if request.user.is_authenticated() else {}
				)
			}
		)

	def post(self, request):
		form = Form_Report(request.POST, request.FILES)
		obj = form.create(request)

		# Object was created, so reset form and send message
		if obj:
			form = Form_Report
			messages.success(request, "Your abuse report has been received. We'll investigate shortly. Thanks!")

		return render(
			request, "support/report.html", {
				"form": form
			}
		)
