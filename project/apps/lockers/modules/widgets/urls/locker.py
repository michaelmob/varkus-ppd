from django.conf.urls import url, include
from lockers.utils import locker_url_patterns
from ..views import locker
from ..models import Widget


urlpatterns = [
	url(r"^example/", locker.WidgetExampleView.as_view(), name="example"),

	url(r"^(?P<slug>[A-z0-9]+)/", include([
		url(r"^(?P<visitor>[0-9]+)/$", locker.WidgetLockView.as_view(model=Widget), name="lock-visitor"),
		url(r"^redirect/(?P<offer_id>[0-9]+)/(?P<visitor>[0-9]+)$", locker.WidgetRedirectView.as_view(model=Widget), name="redirect-visitor"),
	]))
]


urlpatterns += locker_url_patterns(Widget)