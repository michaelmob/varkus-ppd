from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import notifications

urlpatterns = [
	#url(r"^1/postback/$", login_required(postback.post), name="api-postback-send"),
	#url(r"^1/postback-test/$", login_required(notifications.notify), name="api-postback-test"),
]