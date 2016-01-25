import os, json
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib.auth.decorators import login_required
from django.contrib import admin

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