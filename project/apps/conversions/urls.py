from django.conf.urls import url
from .views import notifications

urlpatterns = [
	url(r"^notify/(?P<password>\w+)/$", notifications.receive, name="http-notification-receive"),
]