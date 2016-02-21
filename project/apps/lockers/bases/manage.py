from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect

from ..tables import Table_Locker_Lead, Table_Locker_Click


class View_Overview_Base(View):
	template = None
	model = None
	form = None
	table = None
	maximum = 25

	def get(self, request):
		#if self.form: self.form = self.form(request.POST)

		return render(
			request,
			self.template,
			{
				"locker": self.table.Meta.model.__name__.lower(),
				"table": self.table.create(request),
				"MAX": self.maximum,
				"form": self.form
			}
		)

	# Creation
	def post(self, request):
		# Verify we haven't went over the maximum object count
		if(self.model.objects.filter(user=request.user).count() >= self.maximum):
			messages.error(request, "You have reached the " + self.model.__name__.lower() + " limit. Delete some to create a new one.")
			#request.POST = None
			return self.get(request)

		# Create Object, using model (this would be <Widget> or <List>)
		obj = self.model()

		# Set form with post data and our newly created object
		self.form = self.form(request.POST, instance=obj)

		try:
			self.form.create(request.user)
		except ValueError:
			for error in self.form.errors:
				messages.error(request, "%s field: %s" % \
					(
						error.title(),
						self.form.errors[error][0]
					)
				)

			return self.get(request)

		return redirect(obj.get_type() + "s-manage", obj.code)


class View_Manage_Base(View):
	template = None
	model = None
	form = None

	def obj(self, request, code):
		# Redirect to overview if no code provided
		if not code:
			return redirect(self.model.__name__.lower() + "s")

		# Get object, otherwise redirect to overview
		try:
			return self.model.objects.get(user=request.user, code=code)
		except self.model.DoesNotExist:
			return None


	def get(self, request, code=None):
		obj = self.obj(request, code)

		# Redirect if not existant
		if not obj:
			return redirect(self.model.__name__.lower() + "s")

		return self.get_return(request, obj)


	def get_return(self, request, obj):
		return render(
			request, self.template,
			{
				"locker": self.model.__name__.lower(),
				"form": self.form(instance=obj),
				"obj": obj,
				"leads": Table_Locker_Lead.create(request, obj.earnings.get_leads()),
				"viewers": "Clicks&nbsp;<small>(<strong>%s</strong> clicks in the last 5 minutes)</small>" % obj.earnings.get_viewers(),
				"clicks": Table_Locker_Click.create(request, obj.earnings.get_tokens()),
				"url": request.build_absolute_uri(reverse(self.model.__name__.lower() + "s-locker", args=(obj.code,))),
			}
		)


	def post(self, request, code=None):
		obj = self.obj(request, code)

		# Redirect if not existant
		if not obj:
			return redirect(self.model.__name__.lower() + "s")

		# Pass to _return
		return self.post_return(request, obj)


	def post_return(self, request, obj):
		# Save form data
		self.form(request.POST, instance=obj).save()
		messages.success(request, "Your changes have been saved.")
		
		return self.get_return(request, obj)


class View_Delete_Base(View):
	model = None

	def get(self, request):
		return redirect(self.model.__name__.lower() + "s")

	def post(self, request, code=None):
		try:
			self.model.objects.get(user=request.user, code=code).delete()
			messages.success(request, "Your %s has been deleted." % self.model.__name__.lower())
		except self.model.DoesNotExist:
			messages.error(request, "%s has not been deleted." % self.model.__name__)

		return redirect(self.model.__name__.lower() + "s")
