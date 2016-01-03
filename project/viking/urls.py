import os, json
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib.auth.decorators import login_required
from django.contrib import admin

admin.site.login = login_required(admin.site.login)

handler400 = "site.errors.bad_request_400"
handler403 = "site.errors.permission_denied_403"
handler404 = "site.errors.page_not_found_404"
handler500 = "site.errors.internal_server_error_500"

urlpatterns = [
	# Home
	url(r"^", include("apps.site.urls")),

	# Control Panel / Dashboard
	url(r"^", include("apps.cp.urls")),

	# User
	url(r"^", include("apps.user.urls")),

	# Leads
	url(r"^leads/", include("apps.leads.urls")),

	# API
	url(r"^api/", include("apps.api.urls")),

	# Offers
	url(r"^offers/", include("apps.offers.urls")),

	# Support
	url(r"^support/", include("apps.support.urls")),

	# Billing
	url(r"^billing/", include("apps.billing.urls")),

	# Lockers
	url(r"^", include("apps.lockers.urls")),

	# Admin
	url(r"^admin/", include(admin.site.urls)),

]