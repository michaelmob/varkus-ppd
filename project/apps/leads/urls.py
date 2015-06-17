from django.conf.urls import url

from .views import postback
from .views import unlock
from .models import Deposit

urlpatterns = [
	url(r"^postback-send/$", postback.send, name="postback-send"),
	url(r"^postback-receive/(?P<password>\w+)/$", postback.receive, name="postback-receive"),

	url(r"^request/(?P<token>\w+)/$", unlock.request_access, name="request-access"),
]

Deposit.initiate()
