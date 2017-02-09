from braces import views as braces
from django_tables2 import SingleTableView
from django.conf import settings
from ..models import Invoice
from ..tables import InvoiceTable



class InvoiceListView(braces.LoginRequiredMixin, SingleTableView):
	"""
	View to list a User's invoices in a table.
	"""
	model = Invoice
	table_class = InvoiceTable
	table_pagination = {
		"per_page": settings.ITEMS_PER_PAGE_LARGE
	}


	def get_context_data(self, *args, **kwargs):
		"""
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(*args, **kwargs)
		context["choice"] = self.request.user.billing.choice
		context["data"] = self.request.user.billing.get_data()
		return context


	def get_table_data(self):
		"""
		Returns Invoice queryset.
		"""
		return Invoice.objects.filter(user=self.request.user).order_by("-creation_date")