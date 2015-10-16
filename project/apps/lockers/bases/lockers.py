from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden

from apps.offers.models import Offer
from apps.leads.models import Token


class View_Locker(View):
	template = None
	model = None

	def obj(self, request, code):
		# Redirect to overview if no code provided
		if not code:
			return redirect(model)

		# Get object, otherwise redirect to overview
		try:
			return self.model.objects.get(code=code)
		except self.model.DoesNotExist:
			return None

	def get(self, request, code=None):
		obj = self.obj(request, code)
		
		# Redirect if not existant
		if not obj:
			return redirect("locker-404")

		# Set locker_object for offer click to generate token
		request.session["locker_object"] = (obj.get_name(), obj.code)

		return render(
			request,
			self.template,
			{
				"obj": obj,
				"offers": Offer.get_cache(request, obj)
			}
		)


class View_Unlock(View):
	template = None
	model = None
	token = None

	def obj(self, request, code):
		# Redirect to overview if no code provided
		if not code:
			return redirect(model)

		# Get object, otherwise redirect to overview
		try:
			return self.model.objects.get(code=code)
		except self.model.DoesNotExist:
			return None

	def access(self, request, obj):
		# Get token using request and the locker object
		try:
			self.token = Token.get(request, obj)
		except:
			return False

		# Return access
		return self.token.access()

	def _return(self, request, obj):
		return render(
			request,
			self.template,
			{
				"obj": obj,
				"data": self.token.data
			}
		)

	def get(self, request, code=None):
		# Redirect if not existant
		obj = self.obj(request, code)
		if not obj:
			return redirect("locker-404")

		# Check access
		if not self.access(request, obj):
			return redirect("home")

		return self._return(request, obj)


class View_Poll(View_Unlock):
	def _return(self, request, obj):
		return HttpResponse(reverse(obj.get_name() + "s-unlock", args=(obj.code,)))

	def get(self, request, code=None):
		# Redirect if not existant
		obj = self.obj(request, code)
		if not obj:
			return HttpResponse(reverse("locker-404"))

		# Check access
		if not self.access(request, obj):
			return HttpResponseForbidden("0")

		return self._return(request, obj)