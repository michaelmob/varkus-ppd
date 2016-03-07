from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import dashboard, staff

urlpatterns = [
	url(r"^dashboard/$", login_required(dashboard.index), name="dashboard"),

	url(r"^staff/server/$", login_required(staff.server), name="staff-server"),

	url(r"^dashboard/chart/line.json$", login_required(dashboard.line_chart), name="dashboard-chart-line"),
	url(r"^dashboard/chart/map.json$", login_required(dashboard.map_chart), name="dashboard-chart-map"),
]
