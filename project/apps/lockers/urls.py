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
	url(r"^files/$", login_required(files.Overview.as_view()), name="files"),
	url(r"^files/manage/(?P<code>\w+)/$", login_required(files.Manage.as_view()), name="files-manage"),
	url(r"^files/manage/(?P<code>\w+)/chart/line.json$", login_required(files.Line_Chart.as_view()), name="files-manage-line-chart"),
	url(r"^files/manage/(?P<code>\w+)/delete/$", login_required(files.Delete.as_view()), name="files-manage-delete"),
	url(r"^files/upload/$", login_required(files.Upload.as_view()), name="files-upload"),

	# -- Lists
	url(r"^lists/$", login_required(lists.Overview.as_view()), name="lists"),
	url(r"^lists/manage/(?P<code>\w+)/$", login_required(lists.Manage.as_view()), name="lists-manage"),
	url(r"^lists/manage/(?P<code>\w+)/chart/line.json$", login_required(lists.Line_Chart.as_view()), name="lists-manage-line-chart"),
	url(r"^lists/manage/(?P<code>\w+)/delete/$", login_required(lists.Delete.as_view()), name="lists-manage-delete"),

	# -- Links
	url(r"^links/$", login_required(links.Overview.as_view()), name="links"),
	url(r"^links/manage/(?P<code>\w+)/$", login_required(links.Manage.as_view()), name="links-manage"),
	url(r"^links/manage/(?P<code>\w+)/chart/line.json$", login_required(links.Line_Chart.as_view()), name="links-manage-line-chart"),
	url(r"^links/manage/(?P<code>\w+)/delete/$", login_required(links.Delete.as_view()), name="links-manage-delete"),

	# -- Widgets
	url(r"^widgets/$", login_required(widgets.Overview.as_view()), name="widgets"),
	url(r"^widgets/manage/(?P<code>\w+)/$", login_required(widgets.Manage.as_view()), name="widgets-manage"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/locker/$", login_required(edit_widgets.locker), name="widgets-edit-locker"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/postback/$", login_required(edit_widgets.postback), name="widgets-edit-postback"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/css/$", login_required(edit_widgets.css), name="widgets-edit-css"),
	url(r"^widgets/manage/(?P<code>\w+)/chart/line.json$", login_required(widgets.Line_Chart.as_view()), name="widgets-manage-line-chart"),
	url(r"^widgets/manage/(?P<code>\w+)/delete/$", login_required(widgets.Delete.as_view()), name="widgets-manage-delete"),



	# LOCKERS
	# -- Files
	url(r"^file/(?P<code>\w+)/$", files_locker.Locker.as_view(), name="files-locker"),
	url(r"^file/(?P<code>\w+)/unlock/$", files_locker.Unlock.as_view(), name="files-unlock"),
	url(r"^file/(?P<code>\w+)/download/$", files_locker.Download.as_view(), name="files-download"),

	# -- Lists
	url(r"^list/(?P<code>\w+)/$", lists_locker.Locker.as_view(), name="lists-locker"),
	url(r"^list/(?P<code>\w+)/unlock/$", lists_locker.Unlock.as_view(), name="lists-unlock"),

	# -- Links
	url(r"^link/(?P<code>\w+)/$", links_locker.Locker.as_view(), name="links-locker"),
	url(r"^link/(?P<code>\w+)/unlock/$", links_locker.Unlock.as_view(), name="links-unlock"),

	# -- Widgets
	url(r"^widget/(?P<code>\w+)/$", widgets_locker.Locker.as_view(), name="widgets-locker"),
	url(r"^widget/(?P<code>\w+)/unlock/$", widgets_locker.Unlock.as_view(), name="widgets-unlock"),

	# Locker
	url(r"^lockers/404/$", locker.locker_404, name="locker-404"),

]
