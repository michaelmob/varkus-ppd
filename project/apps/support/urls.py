from django.conf.urls import url

from .views import contact, report

urlpatterns = [
	url(r"^contact/", contact.page, name="contact"),
	url(r"^report/", report.page, name="report"),
]