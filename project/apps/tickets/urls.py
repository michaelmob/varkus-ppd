from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views.manage import View_Overview, View_Manage

urlpatterns = [
	url(r"^$", login_required(View_Overview.as_view()), name="tickets"),
	url(r"^manage/(?P<id>\w+)/$", login_required(View_Manage.as_view()), name="tickets-manage"),
	url(r"^manage/(?P<id>\w+)/(?P<action>\w+)/$", login_required(View_Manage.as_view()), name="tickets-manage-action"),
]