from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import dashboard

urlpatterns = [
	url(r"^dashboard/$", login_required(dashboard.index), name="dashboard"),
	url(r"^staff/$", login_required(dashboard.staff), name="staff"),
]