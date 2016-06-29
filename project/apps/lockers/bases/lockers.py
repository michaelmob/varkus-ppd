from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden

from apps.offers.models import Offer
from apps.conversions.models import Token, Deposit

from utils.geoip import country_code

CRAWLERS = ("googlebot", "slurp", "twiceler", "msnbot", "aloogaot", "yodaobot",
	"baiduspider", "speedy spider", "dotbot", "google favicon", "twitterbot", "telegrambot", "discord")

class View_Locker_Base(View):
	template = None
	model = None

	def obj(self, code):
		# Redirect to overview if no code provided
		if not code:
			return redirect(model)

		# Get object, otherwise redirect to overview
		try:
			return self.model.objects.get(code=code)
		except self.model.DoesNotExist:
			return None

	def deny_crawlers(self, user_agent):
		# Deny webcrwalers and people with no user-agent
		if not user_agent:
			return HttpResponseForbidden("You must have a user-agent to continue")
			
		for c in CRAWLERS:
			if c in user_agent.lower():
				return HttpResponseForbidden("View \"robots.txt\"")

	def get(self, request, code=None):
		# Block bots/webcrawlers
		deny = self.deny_crawlers(request.META.get("HTTP_USER_AGENT", None))
		if deny:
			return deny

		# Set class variables
		self.request = request
		self._obj = self.obj(code)

		# Redirect if not existant
		if not self._obj:
			return redirect("locker-404")

		# Create Session
		if not request.session.exists(request.session.session_key):
			request.session.create()

		# Set unlock if token is set to conversion
		self.unlocked = False
		token = Token.get(request, self._obj)
		if token:
			self.unlocked = token.access()

		return self.get_return()

	def get_return(self):
		ip_address = self.request.META.get("REMOTE_ADDR")
		return render(self.request, self.template, {
			"ip_address": ip_address,
			"country_code": country_code(ip_address),
			"theme": self._obj.theme or "DEFAULT",
			"obj": self._obj,
			"unlocked": self.unlocked,
			"offers": Offer.get_cache(self.request, self._obj)
		})


class View_Redirect_Base(View_Locker_Base):
	model = None

	def get(self, request, code, id=None):
		# Redirect if non-existant
		self._obj = self.obj(code)
		if not self._obj:
			return redirect("locker-404")

		self.request = request
		self.id = id
		return self.get_return()

	def get_return(self):
		try:
			# Retrieve offer if ID is an integer
			int(self.id)
			offer = Offer.objects.get(pk=self.id)

			# Get or create a unique token
			token, created = Token.get_or_create(self.request, self._obj)

			token.offers.add(offer)
			token.save()

		except (KeyError, Offer.DoesNotExist):
			# Offer doesn't exist, or they were directly linked the offer
			return redirect(
				self.request.META.get("HTTP_REFERER", self._obj.get_locker_url()))

		except Token.DoesNotExist:
			# Offer doesn't exist
			return redirect(self._obj.get_locker_url())

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
				self._obj.earnings.increment_clicks()
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
			self.token = Token.get(self.request, self._obj)
			return self.token.access()
		except:
			return False

	def get(self, request, code=None):
		# Set class variables
		self.request = request
		self._obj = self.obj(code)

		# Redirect if not existant
		if not self._obj:
			return redirect("locker-404")

		# Check access
		if not self.access():
			return redirect(self._obj.get_locker_url())

		return self.get_return()

	def get_return(self):
		return render(self.request, self.template, {
			"theme": self._obj.theme or "DEFAULT",
			"obj": self._obj,
			"data": self.data()
		})

	def data(self):
		return self.token.data
