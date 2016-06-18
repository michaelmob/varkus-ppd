from django.conf.urls import url
from .views import notifications, conversions, statistics
#from

urlpatterns = [
	# HTTP Notification
	url(r"^notify/(?P<password>\w+)/$", notifications.receive, name="http-notification-receive"),

	# Conversions
	url(r"^$", conversions.View_Conversions.as_view(), name="conversions"),

	# Statistics
	url(r"^statistics/$", statistics.View_Offers.as_view(), name="statistics"),
	url(r"^statistics/offers/$", statistics.View_Offers.as_view(), name="statistics-offers"),
	url(r"^statistics/countries/", statistics.View_Countries.as_view(), name="statistics-countries"),
]