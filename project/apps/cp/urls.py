from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import dashboard, staff

urlpatterns = [
	url(r"^staff/server/advanced/$", login_required(staff.Advanced.as_view()), name="staff-advanced"),
	url(r"^staff/server/$", login_required(staff.Server.as_view()), name="staff-server"),
	url(r"^staff/server/(?P<action>[\w-]+)/$", login_required(staff.Server.as_view()), name="staff-server-api"),

	url(r"^dashboard/$", login_required(dashboard.index), name="dashboard"),
	url(r"^dashboard/notifications/$", login_required(dashboard.notifications), name="dashboard-notifications"),
	url(r"^dashboard/notifications/(?P<action>\w+)/$", login_required(dashboard.notifications), name="dashboard-notifications-action"),
	url(r"^dashboard/chart/line.json$", login_required(dashboard.line_chart), name="dashboard-chart-line"),
	url(r"^dashboard/chart/map.json$", login_required(dashboard.map_chart), name="dashboard-chart-map"),
]
