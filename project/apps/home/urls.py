from django.conf.urls import url

from . import views
from . import shortcuts

urlpatterns = [
	url(r"^$", views.index, name="home"),
	url(r"^terms/", views.terms, name="terms"),
	url(r"^dmca/", views.dmca, name="dmca"),

	# Shortcuts
	url(r"^r/(?P<referrer>[0-9]+)", shortcuts.signup, name="signup-referral-short"),
]