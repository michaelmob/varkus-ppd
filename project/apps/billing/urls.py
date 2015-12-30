from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import billing

urlpatterns = [
	url(r"^$",
		login_required(billing.View_Overview.as_view()),
		name="billing"),
]
