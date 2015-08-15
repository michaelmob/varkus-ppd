from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import dashboard, leads

urlpatterns = [
	url(r"^dashboard/$", login_required(dashboard.index), name="dashboard"),
	url(r"^staff/$", login_required(dashboard.staff), name="staff"),

	url(r"^staff/info/$", login_required(dashboard.staff_info), name="staff-info"),

	url(r"^dashboard/chart/line.json$", login_required(dashboard.line_chart), name="dashboard-chart-line"),
	url(r"^dashboard/chart/map.json$", login_required(dashboard.map_chart), name="dashboard-chart-map"),

	url(r"^dashboard/leads/$", login_required(leads.index), name="leads"),
	url(r"^dashboard/leads/poll/$", login_required(leads.poll), name="leads-poll"),
]