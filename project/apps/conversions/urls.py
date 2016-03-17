from django.conf.urls import url

from .views import postback
from .views import notifications
from .models import Deposit

urlpatterns = [
	url(r"^notify/(?P<password>\w+)/$", notifications.receive, name="http-notification-receive"),
]
