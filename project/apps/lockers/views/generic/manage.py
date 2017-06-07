from datetime import datetime, timedelta
from importlib import import_module
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin
from django_tables2 import SingleTableView, MultiTableMixin
from controlpanel.views.generic import ActivityChartView
from lockers import tables



class ManageMixin(LoginRequiredMixin):
	"""
	Control Panel management mixin for all manage-based locker views.
	"""
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
		return "%ss/manage/%s%s.html" % (
			self.model_name, self.model_name, self.template_name_suffix
		)


	def get_queryset(self, **kwargs):
		"""
		Queryset for locker objects owned by user.
		"""
		return super(__class__, self).get_queryset(**kwargs).filter(
			user=self.request.user
		)


	def get_context_data(self, **kwargs):
		"""
		Add 'model_name' to context.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		if hasattr(self, "model"):
			context["model_name"] = self.model.__name__.lower()
		return context



class ManageFormMixin(ManageMixin):
	"""
	Modify .get_form_class() method to set placeholders for lockers's forms.
	"""
	def get_placeholders(self):
		"""
		Returns generic placeholders dictionary.
		"""
		if hasattr(self, "placeholders"):
			return self.placeholders

		return {}


	def get_form_class(self):
		"""
		Modify form to set 'items' field to required.
		"""
		form = super(__class__, self).get_form_class()
		for key, value in self.placeholders.items():
			if not key in form.base_fields:
				continue
			form.base_fields[key].widget.attrs["placeholder"] = value
		return form


	def get_initial(self):
		"""
		Return the initial data to use for forms on this view.
		"""
		data = super(__class__, self).get_initial()
		data["access_time_limit"] = str(getattr(self.object, "access_time_limit", "0"))
		return data



class ManageListView(ManageMixin, SingleTableView):
	"""
	Base list view for locker objects.
	"""
	table_pagination = {
		"per_page": settings.ITEMS_PER_PAGE_LARGE
	}


	def __init__(self, *args, **kwargs):
		"""
		Construct the list view.
		Dynamically import table class.
		"""
		self.model = kwargs.get("model", self.model)

		if self.model and not self.table_class:
			name = self.model_name.lower()

			# Dynamically import model's listview table class
			tables = import_module("modules." + name + "s.tables")
			self.table_class = getattr(tables, name.title() + "Table")

		return super(__class__, self).__init__(*args, **kwargs)



	def get_context_data(self, **kwargs):
		"""
		Add 'maximum_objects' to context.
		Returns context.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["maximum_objects"] = self.model.maximum_amount()
		return context


	def get_table_data(self):
		"""
		Returns table data.
		"""
		return self.get_queryset().select_related("earnings")



class ManageDetailView(ManageMixin, MultiTableMixin, DetailView):
	"""
	Base detail view for locker objects.
	"""
	slug_field = "code"
	table_prefix = "t{}-"
	table_pagination = {
		"per_page": settings.ITEMS_PER_PAGE_SMALL
	}


	def get_tables(self, **kwargs):
		"""
		Returns list of tables.
		"""
		clicks_table = tables.LockerClicksTable(
			self.object.earnings.get_tokens()
		)

		conversions_table = tables.LockerConversionsTable(
			self.object.earnings.get_conversions()
		)

		return (clicks_table, conversions_table)


	def get_context_data(self, **kwargs):
		"""
		Add 'visitors' element which contains most recent visitors.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["visitors"] = self.object.earnings.get_tokens((
			datetime.now() - timedelta(minutes=5), datetime.now()
		)).only("pk").count()
		return context



class ManageCreateView(ManageFormMixin, SuccessMessageMixin, CreateView):
	"""
	Base create view for locker objects.
	"""
	template_name_suffix = "_create"
	success_message = ""
	error_message = "Please delete a %(model_name)s before attempting to create a new one."


	@property
	def success_url(self):
		"""
		Returns object's detail URL.
		"""
		return self.object.get_absolute_url()


	def object_count(self):
		"""
		Returns object count for the locker object's model.
		"""
		return self.model.objects.filter(user=self.request.user).count()


	def get(self, request, **kwargs):
		"""
		Disallow user from creating a new locker object if they have exceeded
		their allowed amount.
		Returns parent's .get() method.
		"""
		if self.object_count() >= self.model.maximum_amount():
			messages.error(self.request, self.error_message % {
				"model_name": self.model_name
			})
			return redirect(reverse_lazy(self.model_name + "s:list"))

		return super(__class__, self).get(request, **kwargs)


	def form_valid(self, form):
		"""
		Override .form_valid() method.
		Set 'user' field of object to be created.
		Returns value of parent's .form_valid() method.
		"""
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		return super(__class__, self).form_valid(form)



class ManageDeleteView(ManageMixin, SuccessMessageMixin, DeleteView):
	"""
	Base view for deletion of a locker object.
	"""
	slug_field = "code"
	success_message = "Your %(model_name)s has been deleted."
	template_name_suffix = "_delete"


	@property
	def success_url(self):
		"""
		Returns URL to listview.
		"""
		return reverse_lazy(self.model._meta.model_name + "s:list")


	def delete(self, request, *args, **kwargs):
		"""
		Set success message on delete.
		Returns parent's .delete() method.
		"""
		messages.success(self.request, self.success_message % {
			"model_name": self.model_name
		})
		return super(__class__, self).delete(self, *args, **kwargs)



class ManageUpdateView(ManageMixin, SuccessMessageMixin, UpdateView):
	"""
	Base update view for locker objects.
	"""
	slug_field = "code"
	template_name_suffix = "_update"
	fields = ["name", "description"]
	success_message = "Your %(model_name)s has been updated."


	@property
	def success_url(self):
		"""
		Returns object's detail URL.
		"""
		return self.object.get_absolute_url()


	def get_success_message(self, cleaned_data):
		"""
		Return a modified success_message.
		"""
		return self.success_message % {
			"model_name": self.model_name
		}



class ManageActivityChartView(ManageMixin, ActivityChartView):
	"""
	Base activity chart view for locker objects.
	"""
	slug_field = "code"