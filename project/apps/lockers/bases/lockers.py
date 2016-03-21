from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden

from apps.offers.models import Offer
from apps.conversions.models import Token, Deposit

CRAWLERS = ("googlebot", "slurp", "twiceler", "msnbot", "aloogaot", "yodaobot",
	"baiduspider", "speedy spider", "dotbot", "google favicon")

class View_Locker_Base(View):
	template = None
	model = None

	_request = None
	_obj = None

	def obj(self, code):
		# Redirect to overview if no code provided
		if not code:
			return redirect(model)

		# Get object, otherwise redirect to overview
		try:
			return self.model.objects.get(code=code)
		except self.model.DoesNotExist:
			return None

	def get(self, request, code=None):
		# Deny webcrwalers and people with no user-agent
		UA = request.META.get("HTTP_USER_AGENT", None)
		if not UA:
			return HttpResponseForbidden("You must have a user-agent to continue")
			
		for c in CRAWLERS:
			if c in UA.lower():
				return HttpResponseForbidden("View \"robots.txt\"")

		# Set class variables
		self._request = request
		self._obj = self.obj(code)

		# Redirect if not existant
		if not self._obj:
			return redirect("locker-404")

		# Create Session
		if not request.session.exists(request.session.session_key):
			request.session.create()

		# Set unlock if token is set to conversion
		unlocked = False
		token = Token.get(request, self._obj)
		if token:
			unlocked = token.access()

		return render(
			request,
			self.template,
			{
				"ip_address": request.META.get("REMOTE_ADDR"),
				"theme": self._obj.theme or "DEFAULT",
				"obj": self._obj,
				"unlocked": unlocked,
				"offers": Offer.get_cache(request, self._obj)
			}
		)


class View_Redirect_Base(View_Locker_Base):
	model = None

	def get(self, request, code, id=None):
		# Redirect if non-existant
		self._obj = self.obj(code)
		if not self._obj:
			return redirect("locker-404")

		try:
			# Retrieve offer if ID is an integer
			int(id)
			offer = Offer.objects.get(pk=id)

			# Get or create a unique token
			token, created = Token.get_or_create(request, self._obj)

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
			user = self._obj.user
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

	def access(self):
		# Get token using request and the locker object
		try:
			self.token = Token.get(self._request, self._obj)
		except:
			return False

		# Return access
		return self.token.access()

	def get(self, request, code=None):
		# Set class variables
		self._request = request
		self._obj = self.obj(code)

		# Redirect if not existant
		if not self._obj:
			return redirect("locker-404")

		# Check access
		if not self.access():
			return redirect("home")

		return self.get_return()

	def get_return(self):
		return render(
			self._request,
			self.template,
			{
				"theme": self._obj.theme or "DEFAULT",
				"obj": self._obj,
				"data": self.data()
			}
		)

	def data(self):
		return self.token.data
