from django.conf.urls import url

from .views.contact import View_Contact
from .views.report import View_Report

urlpatterns = [
	url(r"^contact/", View_Contact.as_view(), name="contact"),
	url(r"^report/", View_Report.as_view(), name="report"),
]
