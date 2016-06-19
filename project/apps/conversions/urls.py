from django.conf.urls import url
from .views import notifications, conversions, statistics
from django.contrib.auth.decorators import login_required

urlpatterns = [
	# HTTP Notification
	url(r"^notify/(?P<password>\w+)/$", notifications.receive, name="http-notification-receive"),

	# Conversions
	url(r"^$", login_required(conversions.View_Conversions.as_view()), name="conversions"),

	# Statistics
	url(r"^statistics/$", login_required(statistics.View_Offers.as_view()), name="statistics"),
	url(r"^statistics/offers/$", login_required(statistics.View_Offers.as_view()), name="statistics-offers"),
	url(r"^statistics/countries/", login_required(statistics.View_Countries.as_view()), name="statistics-countries"),
]