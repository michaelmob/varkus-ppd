from django.conf import settings
from django.core.validators import URLValidator
from django.shortcuts import render, redirect

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Redirect_Base
from ..models import Widget


class View_Locker(View_Locker_Base):
	model = Widget
	template = "offers/widget/widget.html"


class View_Redirect(View_Redirect_Base):
	model = Widget


class View_Unlock(View_Unlock_Base):
	template = "offers/widget/complete.html"
	model = Widget

	def get_return(self):
		# We have the locker object, so lets let them unlock it
		if self._obj.locker:
			model = self._obj.locker.get_type()

			# Prevent cust1m exec
			if not model.upper() in dict(settings.LOCKERS).keys():
				return render(self._request, self.template, { })

			# Import Unlock class from locker object's view
			exec("from apps.lockers.%ss.views.locker import View_Unlock as U1" % model.lower(), globals())

			# Vars to be used in U2
			token = self.token
			request = self._request
			obj = self._obj.locker

			# Make child class, with "internal" as True, so if it is a file
			# download the get_return() from the class will allow give it access
			class U2(U1):
				def __init__(self):
					self.internal = True
					self.token = token
					self._request = request
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

		return render(self._request, self.template, { })