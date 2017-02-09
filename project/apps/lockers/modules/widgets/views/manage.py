from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from lockers.views import generic


# Dynamically import locker models
LOCKERS = [x[0].lower()[:6] for x in settings.LOCKERS]
for name in LOCKERS:
	if name.isalpha():
		exec("from modules.%ss.models import %s" % (name, name.title()))



class WidgetMixin(object):
	"""
	Widget mixin to include Widget features to each view.
	"""
	model = Widget



class WidgetFormMixin(generic.ManageFormMixin, WidgetMixin):
	"""
	Modify .get_form_class() method to set placeholders for Widget's forms.
	"""
	placeholders = {
		"name": "My Widget",
		"description": "This is my widget.",
	}

	

class WidgetCreateView(WidgetFormMixin, generic.ManageCreateView):
	"""
	Creation view to create a widget.
	"""
	fields = ["name", "description"]
	


class WidgetUpdateView(WidgetFormMixin, generic.ManageUpdateView):
	"""
	Update view for editing widgets.
	"""
	fields = [
		# Details
		"name", "description",

		# Viral
		"viral_mode", "viral_count",
		"viral_noun", "viral_message",

		# Webhooks
		"webhook_url"
	]


	def get_context_data(self, **kwargs):
		"""
		Add viral_message to context for template.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["viral_message"] = settings.VIRAL_MESSAGE
		return context



class WidgetUpdateLockerView(WidgetMixin, generic.ManageUpdateView):
	"""
	View for setting a Widget's locker pairing.
	"""
	template_name_suffix = "_update_locker"
	fields = ["redirect_url"]


	def get_context_data(self, **kwargs):
		"""
		Add all user's locker objects to context.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["objects"] = {
			model: eval(model.title()).objects.filter(user=self.request.user)
				for model in LOCKERS if not model == "widget"
		}
		context["ref"] = (
			(self.object.locker.type + "," + self.object.locker.code)
				if self.object.locker else None
		)
		return context


	def form_valid(self, form):
		"""
		Get locker's reference value from POST data. Split data by comma and
		get the first two elements of the list. Verify locker's model exists
		then search for object and attempt to set it to locker field.

		Returns the super class .form_valid() method.
		"""
		ref = self.request.POST.get("locker")

		if ref == "redirect":
			self.object.locker = None
			self.object.save()

		elif ref and "," in ref:
			model_name, code = ref.split(",")[:2]

			if model_name in LOCKERS and not model_name == "widget":
				model = eval(model_name.title())
				self.object.locker = (
					model.objects.filter(user=self.request.user, code=code).first()
				)
				self.object.save()

		return super(__class__, self).form_valid(form)



class WidgetUpdateCSSView(WidgetMixin, generic.ManageUpdateView):
	"""
	View for editing the Widget's custom CSS file.
	"""
	template_name_suffix = "_update_css"
	fields = []


	def form_valid(self, form):
		"""
		Save object CSS on form valid.
		"""
		self.object.css = self.request.POST.get("content")
		return super(__class__, self).form_valid(form)



class WidgetUpdateEmbedView(WidgetMixin, generic.ManageUpdateView):
	"""
	View for Embedding a widget.
	"""
	template_name_suffix = "_update_embed"
	fields = []


	def get_context_data(self, **kwargs):
		"""
		Extend context data.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["url"] = self.request.build_absolute_uri(self.object.get_locker_url())
		return context