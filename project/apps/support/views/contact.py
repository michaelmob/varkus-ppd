from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from ..forms import Form_Contact
from ..models import Contact_Message


class View_Contact(View):
	def get(self, request):
		return render(
			request, "support/contact.html", {
				"form": Form_Contact
			}
		)

	def post(self, request):
		form = Form_Contact(request.POST)
		obj = form.create(request)

		# Object was created, so reset form and send message
		if obj:
			form = Form_Contact
			messages.success(request, "Your message has been received. Thanks for your feedback!")

		return render(
			request, "support/contact.html", {
				"form": form
			}
		)
