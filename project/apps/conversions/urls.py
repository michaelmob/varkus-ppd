from django.conf.urls import url

from .views import postback
from .views import notifications
from .models import Deposit

urlpatterns = [
	url(r"^postback-send/$", postback.internal, name="postback-send"),
	url(r"^postback-receive/(?P<password>\w+)/$", postback.receive, name="postback-receive"),

	url(r"^notify/(?P<password>\w+)/$", notifications.receive, name="http-notification-receive"),
]
