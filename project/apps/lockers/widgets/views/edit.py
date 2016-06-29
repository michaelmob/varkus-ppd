from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.validators import URLValidator

from ...bases.manage import View_Overview_Base, View_Manage_Base
from apps.lockers.utils import locker_ref_to_object

from ..forms import Form_Viral
from ..models import Widget
from apps.lockers.files.models import File
from apps.lockers.links.models import Link
from apps.lockers.lists.models import List


class View_Set_Locker(View_Manage_Base):
	template = "widgets/manage/edit/locker.html"
	model = Widget

	def get_return(self, request, obj):
		files = File.objects.filter(user=request.user)
		links = Link.objects.filter(user=request.user)
		lists = List.objects.filter(user=request.user)

		return render(request, self.template, {
			"locker": self.model.__name__.lower(),
			"obj": obj,
			"files": files,
			"links": links,
			"lists": lists,
		})

	def post_return(self, request, obj):
		ref = request.POST.get("locker", None)

		if not ref:
			messages.error(request, "Error pairing a locker to this widget.")
			return self.get_return(request, obj)

		# Standalone Locker
		if ref == "standalone":
			obj.locker = None
			obj.standalone_redirect_url = request.POST.get("redirect", settings.SITE_URL).strip()
			obj.save()
			messages.success(request, "This widget's locker pair has been updated.")

		# Paired Locker
		else:
			locker = locker_ref_to_object(ref, code=True)

			if locker and locker.user == request.user:
				obj.locker = locker
				obj.save()
				messages.success(request, "This widget's locker pair has been updated.")

		return self.get_return(request, obj)


class View_Set_HTTP_Notifications(View_Manage_Base):
	template = "widgets/manage/edit/http-notifications.html"
	model = Widget

	disable_message = "HTTP Notifications have been disabled for this widget."
	edit_message = "HTTP Notifications have been updated."

	field = "http_notification_url"

	def get_return(self, request, obj):
		if(request.GET.get("disable", None) == "1"):
			self.modify_object(obj, None)
			messages.error(request, self.disable_message)
			return redirect("widgets-manage", obj.code)

		return render(request, self.template, {
			"locker": self.model.__name__.lower(),
			"obj": obj
		})

	def post_return(self, request, obj):
		url = request.POST.get(self.field, "").strip()

		validate = URLValidator()
		try:
			validate(url)
			self.modify_object(obj, url)
		except:
			self.modify_object(obj, None)

		messages.success(request, self.edit_message)

		return self.get_return(request, obj)

	def modify_object(self, obj, value):
		obj.http_notification_url = value
		obj.save()


class View_Set_CSS(View_Set_HTTP_Notifications):
	template = "widgets/manage/edit/css.html"
	model = Widget
	
	disable_message = "This widget will no longer use a custom stylesheet."
	edit_message = "This widget custom stylesheet setting has been updated."
	
	field = "custom_css_url"

	def modify_object(self, obj, value):
		obj.custom_css_url = value
		obj.save()


class View_Set_Viral(View_Manage_Base):
	template = "widgets/manage/edit/viral.html"
	model = Widget
	form = Form_Viral

	def get_return(self, request, obj):
		return render(request, self.template, {
			"locker": self.model.__name__.lower(),
			"form": self.form(instance=obj),
			"obj": obj, 
			"message": settings.VIRAL_MESSAGE
		})