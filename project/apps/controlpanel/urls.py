from django.conf.urls import url
from .views import dashboard, notifications, staff


urlpatterns = [
	url(r"^dashboard/$", dashboard.DashboardView.as_view(), name="dashboard"),
	url(r"^dashboard/activity.json$", dashboard.DashboardActivityChartView.as_view(), name="dashboard-activity-chart"),
	url(r"^dashboard/map.json$", dashboard.DashboardMapChartView.as_view(), name="dashboard-map-chart"),
	
	url(r"^notifications/list/", notifications.NotificationsListView.as_view(), name="notifications-list")
]
