from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .utils import sync
from .views import manage

urlpatterns = [

	# Staff Offer Management
	url(r"^sync/",
		sync.sync,
		name="offers-sync"),

	# Options
	url(r"^options/$",
		login_required(manage.View_Options.as_view()),
		name="offers-options"),

	# Offer Management
	url(r"^$",
		login_required(manage.View_Overview.as_view()),
		name="offers"),

	# -- Manage
	url(r"^manage/(?P<id>[0-9]+)/$",
		login_required(manage.View_Manage.as_view()),
		name="offers-manage"),

	# -- Set Importance
	url(r"^manage/(?P<id>[0-9]+)/(?P<importance>\w+)/$",
		login_required(manage.View_Importance.as_view()),
		name="offers-manage-priority"),

	# -- Line Charts
	url(r"^manage/(?P<id>[0-9]+)/chart/line.json$",
		login_required(manage.View_Line_Chart.as_view()),
		name="offers-manage-line-chart"),

]
