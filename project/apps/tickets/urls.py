from django.conf.urls import url
from .views import TicketListView, TicketCreateView, TicketDetailView


app_name = "tickets"

urlpatterns = [
	url(r"^$", TicketListView.as_view(), name="list"),
	url(r"^create/$", TicketCreateView.as_view(), name="create"),
	url(r"^(?P<pk>[0-9]+)/$", TicketDetailView.as_view(), name="detail"),
	url(r"^(?P<pk>[0-9]+)/(?P<action>[A-z]+)/$", TicketDetailView.as_view(), name="detail"),
]