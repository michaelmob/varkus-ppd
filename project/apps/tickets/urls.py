from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [

	url(
		r"^$",
		login_required(views.list),
		name="tickets"
	),

	url(
		r"^p=(?P<page>[0-9]+)/$",
		login_required(views.list),
		name="tickets-page"
	),

	url(
		r"^staff/$",
		login_required(views.staff_list),
		name="staff-tickets"
	),

	url(
		r"^staff/p=(?P<page>[0-9]+)/$",
		login_required(views.staff_list),
		name="staff-tickets-page"
	),

	url(
		r"^(?P<id>[0-9]+)/$",
		login_required(views.thread),
		name="tickets-thread"
	),

	url(
		r"^(?P<id>[0-9]+)/(?P<action>\w+)/$",
		login_required(views.thread),
		name="tickets-thread-action"
	),

]