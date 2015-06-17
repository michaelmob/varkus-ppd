from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib.auth.decorators import login_required
from django.contrib import admin

admin.site.login = login_required(admin.site.login)

urlpatterns = patterns("",
	# Home
	url(r"^", include("apps.home.urls")),

	# Control Panel / Dashboard
	url(r"^", include("apps.cp.urls")),

	# User
	url(r"^user/", include("apps.user.urls")),

	# Leads
	url(r"^leads/", include("apps.leads.urls")),

	# Offers
	url(r"^offers/", include("apps.offers.urls")),

	# Support
	url(r"^support/", include("apps.support.urls")),

	# Tickets
	url(r"^tickets/", include("apps.tickets.urls")),

	# Billing
	url(r"^billing/", include("apps.billing.urls")),

	# Lockers
	url(r"^", include("apps.lockers.urls")),

	# Admin
	url(r"^admin/", include(admin.site.urls)),
) + (
	static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True) +
	static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
