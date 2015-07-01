from django.conf.urls import url

from .views import postback
from .views import unlock
from .models import Deposit

urlpatterns = [
	url(r"^postback-send/$", postback.send, name="postback-send"),
	url(r"^postback-receive/(?P<password>\w+)/$", postback.receive, name="postback-receive"),

	url(r"^poll/(?P<token>\w+)/$", unlock.poll, name="poll-access"),
]

Deposit.initiate()
