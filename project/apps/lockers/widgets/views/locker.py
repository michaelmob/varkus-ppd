from django.conf import settings
from django.core.validators import URLValidator
from django.shortcuts import render, redirect

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Poll_Base, View_Redirect_Base
from ..models import Widget


class View_Locker(View_Locker_Base):
	model = Widget
	template = "offers/widget/widget.html"


class View_Redirect(View_Redirect_Base):
	model = Widget


class View_Unlock(View_Unlock_Base):
	template = "offers/widget/complete.html"
	model = Widget

	def get_return(self, request, obj):
		# We have locker_obj, so lets let them unlock it
		if obj.locker:
			model = obj.locker.get_type()

			# Prevent cust1m exec
			if not model.upper() in dict(settings.LOCKERS).keys():
				return render(request, self.template, { })

			# Import Unlock class from locker object's view
			exec("from apps.lockers.%ss.views.locker import View_Unlock as U1" % model.lower(), globals())

			# Use this token in U2 class
			token = self.token

			# Make child class
			class U2(U1):
				def __init__(self):
					self.token = token

			# Set session key so the download knows to
			# send the file download when the client clicks "Download"
			request.session["locker__file_force"] = True

			# Show Unlock view
			return U2().get_return(request, obj.locker)

		# They didn't have a locker_obj with the widget so
		# check the redirect_url of the widget, and if that
		# URL is not valid then pass through, which will
		# redirect them to a generic survey complete page
		else:
			url = obj.standalone_redirect_url

			try:
				validate = URLValidator()
				validate(url)
				return redirect(url)
			except:
				pass

		return render(request, self.template, { })


class View_Poll(View_Poll_Base):
	model = Widget