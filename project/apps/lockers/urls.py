from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views as locker

from .files.views import manage as files
from .lists.views import manage as lists
from .links.views import manage as links

from .lists.views import locker as lists_locker
from .files.views import locker as files_locker
from .links.views import locker as links_locker


urlpatterns = [

	# Files - Manage
	url(r"^files/$", login_required(files.display), name="files"),
	url(r"^files/(?P<page>[0-9]+)/$", login_required(files.display), name="files-page"),
	url(r"^files/manage/(?P<code>\w+)/$", login_required(files.manage), name="files-manage"),
	url(r"^files/manage/(?P<code>\w+)/delete/$", login_required(files.delete), name="files-manage-delete"),
	url(r"^files/upload/$", login_required(files.upload), name="files-upload"),
	url(r"^files/process/$", login_required(files.process), name="files-process"),

	# Files - Locker
	url(r"^file/(?P<code>\w+)/$", files_locker.locker, name="files-locker"),
	url(r"^file/(?P<code>\w+)/unlock/$", files_locker.unlock, name="files-unlock"),
	url(r"^file/(?P<code>\w+)/download/$", files_locker.download, name="files-download"),

	# Lists - Manage
	url(r"^lists/$", login_required(lists.display), name="lists"),
	url(r"^lists/(?P<page>[0-9]+)/$", login_required(lists.display), name="lists-page"),
	url(r"^lists/manage/(?P<code>\w+)/$", login_required(lists.manage), name="lists-manage"),
	url(r"^lists/manage/(?P<code>\w+)/delete/$", login_required(lists.delete), name="lists-manage-delete"),

	# Lists - Locker
	url(r"^list/(?P<code>\w+)/$", lists_locker.locker, name="lists-locker"),
	url(r"^list/(?P<code>\w+)/unlock/$", lists_locker.unlock, name="lists-unlock"),

	# Links - Manage
	url(r"^links/$", login_required(links.display), name="links"),
	url(r"^links/(?P<page>[0-9]+)/$", login_required(links.display), name="links-page"),
	url(r"^links/manage/(?P<code>\w+)/$", login_required(links.manage), name="links-manage"),
	url(r"^links/manage/(?P<code>\w+)/delete/$", login_required(links.delete), name="links-manage-delete"),

	# Links - Locker
	url(r"^link/(?P<code>\w+)/$", links_locker.locker, name="links-locker"),
	url(r"^link/(?P<code>\w+)/unlock/$", links_locker.unlock, name="links-unlock"),

	# Locker
	url(r"^lockers/404/$", locker.locker_404, name="locker-404"),

]
