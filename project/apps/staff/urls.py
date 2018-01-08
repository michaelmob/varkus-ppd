from django.conf.urls import url, include
from .views import invoices, users, tickets, system


app_name = "staff"

urlpatterns = [
	url(r"^invoices/", include([
		url(r"^$", invoices.InvoiceStaffListView.as_view(), name="invoice-list"),
		url(r"^(?P<pk>[0-9]+)/$", invoices.InvoiceStaffDetailView.as_view(), name="invoice-detail"),
		url(r"^(?P<pk>[0-9]+)/pay/$", invoices.InvoiceStaffUpdateView.as_view(), name="invoice-update"),
	])),

	url(r"^users/", include([
		url(r"^$", users.UserStaffListView.as_view(), name="user-list"),
		url(r"^(?P<pk>[0-9]+)/$", users.UserStaffDetailView.as_view(), name="user-detail"),
	])),

	url(r"^tickets/", include([
		url(r"^$", tickets.TicketStaffListView.as_view(), name="ticket-list"),
	])),

	url(r"^system/", system.SystemView.as_view(), name="system")
]