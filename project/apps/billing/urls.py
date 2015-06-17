from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views.billing import overview, invoice

urlpatterns = [
	url(r"^$", login_required(overview), name="billing"),
	url(r"^(?P<page>[0-9]+)/$", login_required(overview), name="billing-page"),
	url(r"^invoice/(?P<id>[0-9]+)/$", login_required(invoice), name="billing-invoice"),
]
