from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .utils import sync
from .views import manage, output, redirect

urlpatterns = [
	# Output Offers - Standard
	url(r"^output/$", output.public, name="offers-output"),

	# Staff Offer Management
	url(r"^sync/", sync.adgate, name="offers-sync-adgate"),

	# Redirect
	url(r"^redirect/(?P<id>[0-9]+)/(?P<token>\w+)/$", redirect.redirect, name="offers-redirect"),

	# Offer Management
	url(r"^$", login_required(manage.offers), name="offers"),
	url(r"^manage/(?P<id>[0-9]+)/$", login_required(manage.offer), name="offers-manage"),
	url(r"^manage/(?P<id>[0-9]+)/chart/line.json$", login_required(manage.line_chart), name="offers-manage-line-chart"),

	# Priority
	url(r"^manage/$", login_required(manage.priority), name="offers-priority"),
]
