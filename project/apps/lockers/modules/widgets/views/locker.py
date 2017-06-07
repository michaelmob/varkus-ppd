import re
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from viking.utils import urls
from lockers.views import generic
from lockers.utils import view_classes
from ..models import Widget, WidgetVisitor as Visitor



class WidgetLockView(generic.LockerLockView):
	"""
	Custom Lock view for Widget model.
	"""
	def get(self, request, *args, **kwargs):
		"""
		Returns Widget lock page.
		"""
		self.response = super(__class__, self).get(request, *args, **kwargs)

		# Viral mode is enabled
		if self.object.viral_mode and self.object.viral_count > 0:
			self.visitor()

		return self.response
	

	def visitor(self):
		"""
		Modify the 'get' method's response if 'viral_mode' is enabled.
		"""
		# Add visitor to 'visitors' m2m field
		visitor, added = self.object.add_visitor(
			self.request, self.kwargs.get("visitor")
		)

		# Check if user has gotten required amount of visitors
		if visitor.count >= self.object.viral_count:
			return

		# Validate custom URL
		url = urls.unquote(self.request.GET.get("url"))

		# Use default URL | example: url.com/widget/code/{id}
		if not urls.valid(url):
			self.kwargs["visitor"] = visitor.pk
			url = "/".join(self.request.build_absolute_uri().split("/")[:3])
			url += reverse("widget:lock-visitor", kwargs=self.kwargs)

		# Use custom URL | example: custom.com/#{id}
		else:
			if not "id" in url:
				url += "#{id}"
			url = url.replace("{id}", str(visitor.pk))

		# Set response data
		self.response.context_data["visitor"] = visitor
		self.response.context_data["url"] = url
		self.response.context_data["message"] = self.object.get_viral_message(visitor)
		self.response.template_name = "widgets/locker/widget_viral.html"



class WidgetExampleView(TemplateView):
	"""
	Example Widget with mock offers.
	"""
	template_name = "lockers/external.html"


	def get_context_data(self, *args, **kwargs):
		"""
		Add 'preview' to template's context.
		"""
		context = super(__class__, self).get_context_data(*args, **kwargs)
		context["preview"] = True
		context["object"] = None
		return context



class WidgetRedirectView(generic.LockerRedirectView):
	"""
	Custom Redirect view for Widget model.
	"""
	def get(self, request, *args, **kwargs):
		"""
		Custom Redirect view for Widget to prevent exploits.
		"""
		self.object = self.get_object()

		# Viral mode is enabled
		if self.object.viral_mode and self.object.viral_count > 0:
			visitor, created = self.object.add_visitor(
				self.request, self.request.GET.get("v")
			)

			# Disallow user from getting an Offer redirect to complete the offer
			# and skip the viral stage
			if visitor.count < self.object.viral_count:
				return redirect(self.object.get_locker_url())
	
		return super(__class__, self).get(request, *args, **kwargs)



class WidgetUnlockView(generic.LockerUnlockView):
	"""
	Custom unlock view for a Widget.
	"""
	def get(self, request, *args, **kwargs):
		"""
		Returns the dynamic unlock view.
		"""
		response = super(__class__, self).get(request, *args, **kwargs)

		# User must have access to continue
		if not (self.token and self.token.has_access()):
			return response

		# Paired locker
		if self.object.locker:
			return self.paired()

		# Standalone, no pair
		elif self.object.redirect_url:
			return self.standalone()

		return response


	def paired(self):
		"""
		Returns the unlock view for the paired locker.
		"""
		locker = self.object.locker
		action = self.kwargs.get("action")

		# the `get` method of LockerUnlockView of specified locker type
		get = view_classes(locker.__class__, "Locker", "Unlock")
		return get(self.request, pk=locker.pk, token=self.token, object=locker, action=action)


	def standalone(self):
		"""
		Standalone redirect view for when the object is not paired with
		a locker.
		"""
		url = self.object.redirect_url
		if urls.valid(url):
			return redirect(url)