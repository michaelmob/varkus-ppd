from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden

from apps.offers.models import Offer
from apps.leads.models import Token, Deposit


class View_Locker_Base(View):
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

		# Create Session
		if not request.session.exists(request.session.session_key):
			request.session.create()

		# Set unlock if token is set to lead
		unlocked = False
		token = Token.get(request, obj)
		if token:
			unlocked = token.access()

		return render(
			request,
			self.template,
			{
				"ip_address": request.META.get("REMOTE_ADDR"),
				"theme": "default",
				"obj": obj,
				"unlocked": unlocked,
				"offers": Offer.get_cache(request, obj)
			}
		)


class View_Redirect_Base(View_Locker_Base):
	model = None

	def get(self, request, code, id=None):
		# Redirect if not existant
		obj = self.obj(request, code)
		if not obj:
			return redirect("locker-404")

		try:
			# Retrieve offer if ID is an integer
			int(id)
			offer = Offer.objects.get(pk=id)

			# Get or create a unique token
			token, created = Token.get_or_create(request, obj)

			token.offers.add(offer)
			token.save()

		except (KeyError, Offer.DoesNotExist):
			# Offer doesn't exist, or they were directly linked the offer
			return redirect(request.META.get("HTTP_REFERER", "home"))

		except Token.DoesNotExist:
			# Offer doesn't exist
			return redirect("home")

		# Check if there's an Affiliate ID override in settings.py
		try:
			user = obj.user
			aff_id = Deposit.get_by_user_id(user.pk).aff_id
		except:
			aff_id = Deposit.default_aff_id()

		# Increment offer and user's clicks
		try:
			if created:
				offer.earnings.increment_clicks()
				user.earnings.increment_clicks()
				obj.earnings.increment_clicks()
		except:
			pass

		url = str(offer.tracking_url) \
				.replace("{o}", str(offer.offer_id)) \
				.replace("{a}", str(aff_id)) \
				.replace("{u}", str(token.unique))

		return redirect(url)


class View_Unlock_Base(View_Locker_Base):
	template = None
	model = None
	token = None

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
				"theme": "default",
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


class View_Poll_Base(View_Unlock_Base):
	def _return(self, request, obj):
		return HttpResponse(reverse(obj.get_type() + "s-unlock", args=(obj.code,)))

	def get(self, request, code=None):
		# Redirect if not existant
		obj = self.obj(request, code)
		if not obj:
			return HttpResponse(reverse("locker-404"))

		# Check access
		if not self.access(request, obj):
			return HttpResponseForbidden("0")

		return self._return(request, obj)
