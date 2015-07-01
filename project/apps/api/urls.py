from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import postback

urlpatterns = [
	#url(r"^1/postback/$", login_required(postback.post), name="api-postback-send"),
	url(r"^1/postback-test/$", login_required(postback.test), name="api-postback-test"),
]