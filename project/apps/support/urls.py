from django.conf.urls import url
from . import views


app_name = "support"

urlpatterns = [
	url(r"^contact/", views.ContactMessageView.as_view(), name="contact"),
	url(r"^report/", views.AbuseReportView.as_view(), name="report"),
]
