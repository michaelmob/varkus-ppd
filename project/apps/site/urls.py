from django.conf.urls import url

from . import views

urlpatterns = [
	url(r"^$", 			views.homepage, name="home"),
	url(r"^terms/", 	views.terms, 	name="terms"),
	url(r"^dmca/", 		views.dmca, 	name="dmca"),
	url(r"^privacy/", 	views.privacy, 	name="privacy"),
]
