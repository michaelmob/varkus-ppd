from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from . import views
from .utils import sync

urlpatterns = [

	# Staff Offer Management
	url(r"^sync/", views.OfferSyncView.as_view(), name="sync"),

	# Offer
	url(r"^$", views.OfferListView.as_view(), name="list"),
	url(r"^(?P<pk>[0-9]+)/$", views.OfferDetailView.as_view(), name="detail"),
	url(r"^(?P<pk>[0-9]+).json$", views.OfferAjaxView.as_view(), name="detail-ajax"),
	url(r"^(?P<pk>[0-9]+)/(?P<action>[\w-]+)/$", views.OfferAjaxView.as_view(), name="detail-ajax-action"),
	url(r"^(?P<pk>[0-9]+)/activity.json$", views.OfferActivityChartView.as_view(), name="activity"),

]
