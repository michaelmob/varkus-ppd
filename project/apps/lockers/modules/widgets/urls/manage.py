from django.conf.urls import url, include
from lockers.utils import manage_url_patterns
from ..views import manage
from ..models import Widget


app_name = "widgets"
urlpatterns = manage_url_patterns(Widget)

urlpatterns += [
	url(r"^(?P<slug>[A-z0-9]+)/", include([
		url(r"^edit/css/$", manage.WidgetUpdateCSSView.as_view(), name="update-css"),
		url(r"^edit/locker/$", manage.WidgetUpdateLockerView.as_view(), name="update-locker"),
		url(r"^edit/embed/$", manage.WidgetUpdateEmbedView.as_view(), name="update-embed"),
	])),
]
