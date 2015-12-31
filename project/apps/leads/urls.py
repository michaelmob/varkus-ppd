from django.conf.urls import url

from .views import postback
from .models import Deposit

urlpatterns = [
	url(r"^postback-send/$", postback.internal, name="postback-send"),
	url(r"^postback-receive/(?P<password>\w+)/$", postback.receive, name="postback-receive"),
]

# Initiate deposits every run
Deposit.initiate()
