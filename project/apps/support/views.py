from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import ContactMessageForm, AbuseReportForm



class ContactMessageView(SuccessMessageMixin, CreateView):
	"""
	View for an anonymous user to send a message to staff.
	"""
	form_class = ContactMessageForm
	template_name = "support/contact_form.html"
	success_message = "Your message has been received."
	success_url = reverse_lazy("support:contact")


	def get_initial(self):
		"""
		Return form initial values.
		"""
		user = self.request.user

		if not user.is_authenticated():
			return {}

		return {
			"name": "%s %s" % (user.first_name, user.last_name),
			"email": user.email
		}


	def form_valid(self, form):
		"""
		Modify form instance before committing.
		"""
		form.instance.ip_address = self.request.META.get("REMOTE_ADDR")
		return super(__class__, self).form_valid(form)



class AbuseReportView(ContactMessageView):
	"""
	View for service abuses to be reported.
	"""
	form_class = AbuseReportForm
	template_name = "support/report_form.html"
	success_message = "Your abuse report has been received."
	success_url = reverse_lazy("support:report")


	def get_initial(self):
		"""
		Add initial 'content' to message field.
		"""
		initial = super(__class__, self).get_initial()
		content = self.request.GET.get("content")

		try:
			URLValidator()(content)
		except:
			pass

		if content:
			initial["message"] = (
				"Content: %s\n"
				"Include additional information below this line ---"
			) % content

		return initial