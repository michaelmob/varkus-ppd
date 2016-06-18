from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from ..forms import Form_Contact
from ..models import Contact_Message


class View_Contact(View):
	def get(self, request):
		return render(
			request, "support/contact.html", {
				"form": Form_Contact(request)
			}
		)

	def post(self, request):
		obj = Form_Contact(request).save()

		if obj:
			messages.success(request, "Your message has been received. Thanks for your feedback!")

		return redirect("contact")
