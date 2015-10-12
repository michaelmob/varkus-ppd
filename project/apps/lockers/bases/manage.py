from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect


class View_Overview(View):
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
				"table": self.table.create(request),
				"MAX": self.maximum,
				"form": self.form
			}
		)

	# Creation
	def post(self, request):
		# Verify we haven't went over the maximum
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

		return redirect(obj.get_name().lower() + "s-manage", obj.code)


class View_Manage(View):
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

		return render(
			request, self.template,
			{
				"url": request.build_absolute_uri(reverse(self.model.__name__.lower() + "s-locker", args=(code,))),
				"form": self.form(instance=obj),
				"obj": obj
			}
		)

	def post(self, request, code=None):
		obj = self.obj(request, code)
		
		# Redirect if not existant
		if not obj:
			return redirect(self.model.__name__.lower() + "s")

		# Save form data
		form = self.form(request.POST, instance=obj)
		form.save()

		return self.get(request, code)


class Delete_Base(View):
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