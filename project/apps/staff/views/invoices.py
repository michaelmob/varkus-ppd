import json
from braces import views as braces
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django_tables2 import SingleTableView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from billing.models import Invoice
from controlpanel.models import Notification
from ..tables import InvoiceStaffTable



class InvoiceStaffuserMixin(braces.LoginRequiredMixin, braces.StaffuserRequiredMixin):
	"""
	Mixin allowing only Staff users to access page.
	"""
	model = Invoice



class InvoiceStaffListView(InvoiceStaffuserMixin, SingleTableView):
	"""
	List Invoices for Staff user.
	"""
	template_name = "staff/invoice_staff_list.html"
	table_class = InvoiceStaffTable


	def get_queryset(self):
		"""
		Get queryset with optional 'user_id' finding.
		"""
		try:
			kwargs = {"user": int(self.request.GET.get("user_id"))}
		except:
			kwargs = {}

		return Invoice.objects.filter(**kwargs).prefetch_related("user")



class InvoiceStaffDetailView(InvoiceStaffuserMixin, DetailView):
	"""
	Detailed Invoice view for Staff user.
	"""
	template_name = "staff/invoice_staff_detail.html"


	def get_context_data(self, *args, **kwargs):
		"""
		Modify context dictionary.
		"""
		context = super(__class__, self).get_context_data(*args, **kwargs)

		try:
			billing = self.request.user.billing
			payment_data = json.loads(billing.data)
			context["payment_data"] = payment_data.get(billing.choice)
		except:
			context["payment_data"] = None

		return context



class InvoiceStaffUpdateView(SuccessMessageMixin, UpdateView, InvoiceStaffDetailView):
	"""
	Detailed Invoice view for Staff user.
	"""
	template_name = "staff/invoice_staff_update.html"
	fields = ("paid", "error", "notes", "file")
	success_message = "Invoice has been updated!"


	@property
	def success_url(self):
		"""
		Returns URL to redirect to on successful update.
		"""
		return reverse_lazy("staff:invoice-detail", args=(self.object.pk,))


	def form_valid(self, form):
		"""
		Optionally notify user that their payment has been marked.
		"""
		kwargs = {
			"recipient": self.object.user,
			"url": reverse_lazy("billing:list")
		}

		if form.cleaned_data["paid"]:
			kwargs["icon"] = "check"
			kwargs["content"] = "Your invoice has been marked as paid!"
			Notification.objects.create_notification(**kwargs)

		elif form.cleaned_data["error"]:
			kwargs["icon"] = "ban"
			kwargs["content"] = "Your invoice has been marked with an error!"
			Notification.objects.create_notification(**kwargs)

		return super(__class__, self).form_valid(form)


	def get_context_data(self, *args, **kwargs):
		"""
		Modify context dictionary.
		"""
		context = super(__class__, self).get_context_data(*args, **kwargs)

		try:
			billing = self.request.user.billing
			payment_data = json.loads(billing.data)
			context["payment_data"] = payment_data.get(billing.choice)
		except:
			context["payment_data"] = None

		return context