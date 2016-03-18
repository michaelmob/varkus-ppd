from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views as locker

from .files.views 	import manage as files
from .lists.views 	import manage as lists
from .links.views 	import manage as links
from .widgets.views import manage as widgets
from .widgets.views import edit   as edit_widgets

from .lists.views 	import locker as lists_locker
from .files.views 	import locker as files_locker
from .links.views 	import locker as links_locker
from .widgets.views import locker as widgets_locker


urlpatterns = [

	# MANAGE
	# -- Files
	url(r"^files/$", login_required(files.View_Overview.as_view()), name="files"),
	url(r"^files/manage/(?P<code>\w+)/$", login_required(files.View_Manage.as_view()), name="files-manage"),
	url(r"^files/manage/(?P<code>\w+)/chart/line.json$", login_required(files.View_Line_Chart.as_view()), name="files-manage-line-chart"),
	url(r"^files/manage/(?P<code>\w+)/delete/$", login_required(files.View_Delete.as_view()), name="files-manage-delete"),
	url(r"^files/upload/$", login_required(files.View_Upload.as_view()), name="files-upload"),

	# -- Lists
	url(r"^lists/$", login_required(lists.View_Overview.as_view()), name="lists"),
	url(r"^lists/manage/(?P<code>\w+)/$", login_required(lists.View_Manage.as_view()), name="lists-manage"),
	url(r"^lists/manage/(?P<code>\w+)/chart/line.json$", login_required(lists.View_Line_Chart.as_view()), name="lists-manage-line-chart"),
	url(r"^lists/manage/(?P<code>\w+)/delete/$", login_required(lists.View_Delete.as_view()), name="lists-manage-delete"),

	# -- Links
	url(r"^links/$", login_required(links.View_Overview.as_view()), name="links"),
	url(r"^links/manage/(?P<code>\w+)/$", login_required(links.View_Manage.as_view()), name="links-manage"),
	url(r"^links/manage/(?P<code>\w+)/chart/line.json$", login_required(links.View_Line_Chart.as_view()), name="links-manage-line-chart"),
	url(r"^links/manage/(?P<code>\w+)/delete/$", login_required(links.View_Delete.as_view()), name="links-manage-delete"),

	# -- Widgets
	url(r"^widgets/$", login_required(widgets.View_Overview.as_view()), name="widgets"),
	url(r"^widgets/manage/(?P<code>\w+)/$", login_required(widgets.View_Manage.as_view()), name="widgets-manage"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/locker/$", login_required(edit_widgets.View_Set_Locker.as_view()), name="widgets-edit-locker"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/http-notifications/$", login_required(edit_widgets.View_Set_HTTP_Notifications.as_view()), name="widgets-edit-http-notifications"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/css/$", login_required(edit_widgets.View_Set_CSS.as_view()), name="widgets-edit-css"),
	url(r"^widgets/manage/(?P<code>\w+)/chart/line.json$", login_required(widgets.View_Line_Chart.as_view()), name="widgets-manage-line-chart"),
	url(r"^widgets/manage/(?P<code>\w+)/delete/$", login_required(widgets.View_Delete.as_view()), name="widgets-manage-delete"),


	# LOCKERS
	# -- Files
	url(r"^file/(?P<code>\w+)/$", files_locker.View_Locker.as_view(), name="files-locker"),
	url(r"^file/(?P<code>\w+)/unlock/$", files_locker.View_Unlock.as_view(), name="files-unlock"),
	url(r"^file/(?P<code>\w+)/download/$", files_locker.View_Download.as_view(), name="files-download"),
	url(r"^file/(?P<code>\w+)/redirect/(?P<id>[0-9]+)$", files_locker.View_Redirect.as_view(), name="files-redirect"),

	# -- Lists
	url(r"^list/(?P<code>\w+)/$", lists_locker.View_Locker.as_view(), name="lists-locker"),
	url(r"^list/(?P<code>\w+)/unlock/$", lists_locker.View_Unlock.as_view(), name="lists-unlock"),
	url(r"^list/(?P<code>\w+)/redirect/(?P<id>[0-9]+)$", lists_locker.View_Redirect.as_view(), name="lists-redirect"),

	# -- Links
	url(r"^link/(?P<code>\w+)/$", links_locker.View_Locker.as_view(), name="links-locker"),
	url(r"^link/(?P<code>\w+)/unlock/$", links_locker.View_Unlock.as_view(), name="links-unlock"),
	url(r"^link/(?P<code>\w+)/redirect/(?P<id>[0-9]+)$", links_locker.View_Redirect.as_view(), name="links-redirect"),

	# -- Widgets
	url(r"^widget/(?P<code>\w+)/$", widgets_locker.View_Locker.as_view(), name="widgets-locker"),
	url(r"^widget/(?P<code>\w+)/unlock/$", widgets_locker.View_Unlock.as_view(), name="widgets-unlock"),
	url(r"^widget/(?P<code>\w+)/redirect/(?P<id>[0-9]+)$", widgets_locker.View_Redirect.as_view(), name="widgets-redirect"),

	# Locker
	url(r"^lockers/404/$", locker.locker_404, name="locker-404"),

]
