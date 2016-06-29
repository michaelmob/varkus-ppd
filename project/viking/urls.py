from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.site.login = login_required(admin.site.login)

handler400 = "apps.site.errors._400"
handler403 = "apps.site.errors._403"
handler404 = "apps.site.errors._404"
handler500 = "apps.site.errors._500"

urlpatterns = [
	# Home
	url(r"^", include("apps.site.urls")),

	# Control Panel / Dashboard
	url(r"^", include("apps.cp.urls")),

	# User
	url(r"^", include("apps.user.urls")),

	# Conversions
	url(r"^conversions/", include("apps.conversions.urls")),

	# Offers
	url(r"^offers/", include("apps.offers.urls")),

	# Support
	url(r"^support/", include("apps.support.urls")),

	# Support
	url(r"^tickets/", include("apps.tickets.urls")),

	# Billing
	url(r"^billing/", include("apps.billing.urls")),

	# Lockers
	url(r"^", include("apps.lockers.urls")),

	# Admin
	url(r"^admin/", include(admin.site.urls)),
]

if settings.DEBUG:
	from django.views.static import serve
	
	urlpatterns += [
		url(r"^media/(?P<path>.*)$", serve, {
			"document_root": settings.MEDIA_ROOT })
	]
