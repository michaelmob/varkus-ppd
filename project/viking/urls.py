from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required


admin.site.login = login_required(admin.site.login)


handler400 = "core.errors._400"
handler403 = "core.errors._403"
handler404 = "core.errors._404"
handler500 = "core.errors._500"


urlpatterns = [
	# Core
	url(r"^", include("core.urls")),

	# Control Panel / Dashboard
	url(r"^", include("controlpanel.urls")),

	# Users
	url(r"^", include("users.urls")),

	# Lockers
	url(r"^", include("lockers.urls")),

	# Conversions
	url(r"^conversions/", include("conversions.urls")),

	# Offers
	url(r"^offers/", include("offers.urls", namespace="offers")),

	# Support
	url(r"^support/", include("support.urls", namespace="support")),

	# Tickets
	url(r"^tickets/", include("tickets.urls", namespace="tickets")),

	# Billing
	url(r"^billing/", include("billing.urls", namespace="billing")),

	# Staff
	url(r"^staff/", include("staff.urls", namespace="staff")),

	# Admin
	url(r"^admin/", include(admin.site.urls)),
]


if settings.DEBUG:
	# debug toolbar
	import debug_toolbar
	urlpatterns += [
		url(r"^__debug__/", include(debug_toolbar.urls))
	]

	# serve media files
	from django.views.static import serve
	urlpatterns += [
		url(r"^media/(?P<path>.*)$", serve, {
			"document_root": settings.MEDIA_ROOT 
		})
	]