from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from ..forms import Form_Thread, Form_Post
from ..tables import Table_Tickets
from ..models import Thread

class View_Overview(View):
	def get(self, request):
		return render(request, "tickets/overview.html", {
			"form": Form_Thread(request),
			"table": Table_Tickets(request)
		})

	def post(self, request):
		obj = Form_Thread(request).save()

		if obj:
			messages.success(request, "Your ticket has been created!")
			return redirect("tickets-manage", id=obj.id)
		else:
			messages.error(request, "Something went wrong in the creation of " +
				"your ticket, please try again.")

		return self.get(request)


class View_Manage(View):
	_obj = None

	def obj(self, id, user):
		if user.is_staff:
			return Thread.objects.filter(id=id).first()

		return Thread.objects.filter(id=id, user=user).first()

	def api(self, action):
		result = {
			"success": True,
			"message": "Ticket status has been updated.",
			"data": {
				"status": "unknown"
			}
		}

		if action == "close":
			result["data"]["status"] = "CLOSED"
			self._obj.closed = True

		elif action == "open":
			result["data"]["status"] = "OPEN"
			self._obj.closed = False

		else:
			result["success"] = False
			result["message"] = "Unknown action."

		self._obj.save()

		return JsonResponse(result)

	def get(self, request, id, action=None):
		if not self._obj:
			self._obj = self.obj(id, request.user)

		if not self._obj:
			return redirect("tickets")

		if action:
			return self.api(action)

		return render(request, "tickets/manage.html", {
			"form": Form_Post(request, self._obj),
			"obj": self._obj
		})

	def post(self, request, id):
		self._obj = self.obj(id, request.user)

		if Form_Post(request, self._obj).save():
			messages.success(request, "Your post has been created!")
		else:
			messages.error(request, "Something went wrong in the creation of" +
				" your post, please try again.")

		return self.get(request, id)