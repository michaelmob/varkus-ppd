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
	url(r"^files/$", login_required(files.display), name="files"),
	url(r"^files/(?P<page>[0-9]+)/$", login_required(files.display), name="files-page"),
	url(r"^files/manage/(?P<code>\w+)/$", login_required(files.manage), name="files-manage"),
	url(r"^files/manage/(?P<code>\w+)/chart/line.json$", login_required(files.line_chart), name="files-manage-line-chart"),
	url(r"^files/manage/(?P<code>\w+)/delete/$", login_required(files.delete), name="files-manage-delete"),
	url(r"^files/upload/$", login_required(files.upload), name="files-upload"),
	url(r"^files/process/$", login_required(files.process), name="files-process"),

	# -- Lists
	url(r"^lists/$", login_required(lists.display), name="lists"),
	url(r"^lists/(?P<page>[0-9]+)/$", login_required(lists.display), name="lists-page"),
	url(r"^lists/manage/(?P<code>\w+)/$", login_required(lists.manage), name="lists-manage"),
	url(r"^lists/manage/(?P<code>\w+)/chart/line.json$", login_required(lists.line_chart), name="lists-manage-line-chart"),
	url(r"^lists/manage/(?P<code>\w+)/delete/$", login_required(lists.delete), name="lists-manage-delete"),

	# -- Links
	url(r"^links/$", login_required(links.display), name="links"),
	url(r"^links/(?P<page>[0-9]+)/$", login_required(links.display), name="links-page"),
	url(r"^links/manage/(?P<code>\w+)/$", login_required(links.manage), name="links-manage"),
	url(r"^links/manage/(?P<code>\w+)/chart/line.json$", login_required(links.line_chart), name="links-manage-line-chart"),
	url(r"^links/manage/(?P<code>\w+)/delete/$", login_required(links.delete), name="links-manage-delete"),

	# -- Widgets
	url(r"^widgets/$", login_required(widgets.display), name="widgets"),
	url(r"^widgets/(?P<page>[0-9]+)/$", login_required(widgets.display), name="widgets-page"),
	url(r"^widgets/manage/(?P<code>\w+)/$", login_required(widgets.manage), name="widgets-manage"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/locker/$", login_required(edit_widgets.locker), name="widgets-edit-locker"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/postback/$", login_required(edit_widgets.postback), name="widgets-edit-postback"),
	url(r"^widgets/manage/(?P<code>\w+)/edit/css/$", login_required(edit_widgets.css), name="widgets-edit-css"),
	url(r"^widgets/manage/(?P<code>\w+)/chart/line.json$", login_required(widgets.line_chart), name="widgets-manage-line-chart"),
	url(r"^widgets/manage/(?P<code>\w+)/delete/$", login_required(widgets.delete), name="widgets-manage-delete"),



	# LOCKERS
	# -- Files
	url(r"^file/(?P<code>\w+)/$", files_locker.locker, name="files-locker"),
	url(r"^file/(?P<code>\w+)/unlock/$", files_locker.unlock, name="files-unlock"),
	url(r"^file/(?P<code>\w+)/download/$", files_locker.download, name="files-download"),

	# -- Lists
	url(r"^list/(?P<code>\w+)/$", lists_locker.locker, name="lists-locker"),
	url(r"^list/(?P<code>\w+)/unlock/$", lists_locker.unlock, name="lists-unlock"),

	# -- Links
	url(r"^link/(?P<code>\w+)/$", links_locker.locker, name="links-locker"),
	url(r"^link/(?P<code>\w+)/unlock/$", links_locker.unlock, name="links-unlock"),

	# -- Widgets
	url(r"^widget/complete/$", widgets_locker.complete, name="widgets-complete"),
	url(r"^widget/(?P<code>\w+)/$", widgets_locker.locker, name="widgets-locker"),
	url(r"^widget/(?P<code>\w+)/unlock/$", widgets_locker.unlock, name="widgets-unlock"),

	# Locker
	url(r"^lockers/404/$", locker.locker_404, name="locker-404"),

]
