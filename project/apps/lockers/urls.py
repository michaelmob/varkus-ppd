from django.conf.urls import url, include



urlpatterns = [
	# Management Views
	url(r"^widgets/", include("modules.widgets.urls.manage", namespace="widgets")),
	url(r"^files/", include("modules.files.urls.manage", namespace="files")),
	url(r"^links/", include("modules.links.urls.manage", namespace="links")),
	url(r"^lists/", include("modules.lists.urls.manage", namespace="lists")),

	# Locking Views
	url(r"^widget/", include("modules.widgets.urls.locker", namespace="widget")),
	url(r"^file/", include("modules.files.urls.locker", namespace="file")),
	url(r"^link/", include("modules.links.urls.locker", namespace="link")),
	url(r"^list/", include("modules.lists.urls.locker", namespace="list")),
]