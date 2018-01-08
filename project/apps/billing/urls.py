from django.conf.urls import url
from .views import invoices, billing


app_name = "billing"

urlpatterns = [
	url(r"^$", invoices.InvoiceListView.as_view(), name="list"),
	url(r"^update/$", billing.BillingUpdateView.as_view(), name="update"),
]
