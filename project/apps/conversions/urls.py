from django.conf.urls import url
from .views import webhooks, conversions, statistics
from django.contrib.auth.decorators import login_required

urlpatterns = [
	# HTTP Notification
	url(r"^notify/(?P<password>\w+)/$", webhooks.receive_payload, name="webhook-receive"),

	# Conversions
	url(r"^$", login_required(conversions.ConversionsView.as_view()), name="conversions"),

	# Statistics
	url(r"^statistics/$", login_required(statistics.OffersView.as_view()), name="statistics"),
	url(r"^statistics/offers/$", login_required(statistics.OffersView.as_view()), name="statistics-offers"),
	url(r"^statistics/countries/", login_required(statistics.CountriesView.as_view()), name="statistics-countries"),
]