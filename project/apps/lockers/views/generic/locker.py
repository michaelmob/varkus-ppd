from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from offers.models import Offer
from conversions.models import Token, Boost
from viking.utils import geoip



class LockerMixin():
	"""
	External content-locking views for all locker-based views.
	"""
	model = None
	slug_field = "code"


	@property
	def model_name(self):
		"""
		Returns model name.
		"""
		return self.model._meta.model_name


	@property
	def template_name(self):
		"""
		Returns template location.
		"""
		return "%ss/locker/%s%s.html" % (
			self.model_name, self.model_name, self.template_name_suffix
		)


	def get(self, request, *args, **kwargs):
		"""
		Disallow crawlers.
		"""
		if not request.META.get("HTTP_USER_AGENT"):
			return HttpResponseForbidden("User-agent required.")

		return super(__class__, self).get(request, *args, **kwargs)


	def get_object(self, *args, **kwargs):
		"""
		Prevent duplicate querying for same object.
		"""
		if hasattr(self, "object"):
			return self.object
		return super(__class__, self).get_object(*args, **kwargs)


	def get_context_data(self, **kwargs):
		"""
		Modify context data.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["token"] = self.token if hasattr(self, "token") else None
		if hasattr(self, "model"):
			context["model_name"] = self.model.__name__.lower()
		return context



class LockerLockView(LockerMixin, DetailView):
	"""
	Base lock view for locker objects.
	"""
	template_name_suffix = "_lock"


	def get_context_data(self, **kwargs):
		"""
		Modify context data.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)

		# Token and Offers
		context["token"] = Token.objects.get_token(self.request, self.object)
		context["offers"] = Offer.objects.get_offers(
			self.request, self.object, count=self.object.offer_count
		)

		# User
		context["ip_address"] = self.request.META.get("REMOTE_ADDR")
		context["country_code"] = geoip.country_code(context["ip_address"])

		return context



class LockerRedirectView(LockerMixin, DetailView):
	"""
	Base redirect view for redirecting a user from a locked page to an offer
	and generating a unique token along the way.
	"""
	def get_offer(self):
		"""
		Return Offer object.
		"""
		offer_id = self.kwargs.get("offer_id")

		try:
			# Find offer
			int(offer_id)
			obj = Offer.objects.get(id=offer_id)
		except Offer.DoesNotExist:
			raise Http404(
				_("No %(verbose_name)s found matching the query") % {
					"verbose_name": Offer._meta.verbose_name
				}
			)

		return obj


	def get_or_create_token(self):
		"""
		Returns Token or creates it if it does not exist.
		"""
		return Token.objects.get_or_create_token(
			self.request, self.object, self.offer
		)

	
	def get(self, request, slug, offer_id, **kwargs):
		"""
		Returns redirection result.
		"""
		# Get objects
		self.offer = self.get_offer()
		self.object = self.get_object()
		self.token, created = self.get_or_create_token()
		self.user = self.object.user

		# Increment clicks
		if created:
			self.offer.earnings.increment_clicks()
			self.object.earnings.increment_clicks()
			if self.user:
				self.user.earnings.increment_clicks()

		# Boost
		if created:
			boost = Boost.objects.filter(user=self.user, offer=self.offer).first()

			if boost:
				if boost.count <= 1:
					boost.delete()
				else:
					boost.decrement_clicks()

		return redirect(self.offer.get_tracking_url(self.offer, self.token))



class LockerUnlockView(LockerMixin, DetailView):
	"""
	Base unlock view for locker objects.
	"""
	template_name_suffix = "_unlock"
	internal = False


	def get_token(self):
		"""
		Returns Token object.
		"""
		return Token.objects.get_token(self.request, self.object)


	def access(self):
		"""
		Response for when the user has access to the material.
		"""
		return


	def get(self, request, **kwargs):
		"""
		Prevent non-authorized user from viewing unlocked object.
		"""
		self.request = request
		self.object = kwargs.get("object") or self.get_object()
		self.token = kwargs.get("token") or self.get_token()

		# User has access
		if self.token and self.token.has_access:
			response = self.access()
			return response or super(__class__, self).get(self.request)

		# User has no access, redirect to locker url
		return redirect(self.object.get_locker_url())