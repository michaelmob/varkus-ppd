import urllib.parse

from django.conf import settings
from django.core.validators import URLValidator
from django.shortcuts import render, redirect

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Redirect_Base
from ..models import Widget, Widget_Visitor as Visitor


class View_Locker(View_Locker_Base):
	model = Widget
	template = "widgets/locker/widget.html"

	def get_return(self):
		# Viral Mode
		if self._obj.viral_mode and self._obj.viral_visitor_count > 0:
			visitor, created = self._obj.visitor(
				self.request, self.request.GET.get("v")
			)

			try:
				validate = URLValidator()
				url = urllib.parse.unquote(self.request.GET.get("url")) 
				validate(url)
			except:
				url = self.request.build_absolute_uri().split("?")[0]

			url += "?v=" + str(visitor.pk)

			if visitor.visitor_count < self._obj.viral_visitor_count:
				return render(self.request, "widgets/locker/viral.html", {
					"obj": self._obj,
					"unlocked": self.unlocked,
					"visitor": visitor,
					"message": self._obj.viral_message_formatted(visitor),
					"url": url
				})

		return super(__class__, self).get_return()


class View_Redirect(View_Redirect_Base):
	model = Widget

	# Override, don't let them do the offer if they havent gotten the right
	# amount of clicks
	def get_return(self):
		# Viral Mode
		if self._obj.viral_mode and self._obj.viral_visitor_count > 0:
			visitor, created = self._obj.visitor(
				self.request, self.request.GET.get("v")
			)

			if visitor.visitor_count < self._obj.viral_visitor_count:
				return redirect(self._obj.get_locker_url())

		return super(__class__, self).get_return()

class View_Unlock(View_Unlock_Base):
	template = "widgets/locker/complete.html"
	model = Widget

	def get_return(self):
		# We have the locker object, so lets let them unlock it
		if self._obj.locker:
			model = self._obj.locker.get_type()

			# Prevent cust1m exec
			if not model.upper() in dict(settings.LOCKERS).keys():
				return render(self.request, self.template)

			# Import Unlock class from locker object's view
			exec("from apps.lockers.%ss.views.locker import View_Unlock as U1" % model.lower(), globals())

			# Vars to be used in U2
			token = self.token
			request = self.request
			obj = self._obj.locker

			# Make child class, with "internal" as True, so if it is a file
			# download the get_return() from the class will allow give it access
			class U2(U1):
				def __init__(self):
					self.internal = True
					self.token = token
					self.request = request
					self._obj = obj

			# Show Unlock view
			return U2().get_return()

		# They didn't have a locker_obj with the widget so
		# check the redirect_url of the widget, and if that
		# URL is not valid then pass through, which will
		# redirect them to a generic survey complete page
		else:
			url = self._obj.standalone_redirect_url

			try:
				validate = URLValidator()
				validate(url)
				return redirect(url)
			except:
				pass

		return render(self.request, self.template)