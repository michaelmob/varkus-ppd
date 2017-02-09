from django.conf.urls import url
from .views import static


urlpatterns = [
	url(r"^$", 			static.homepage, 	name="home"),
	url(r"^terms/", 	static.terms, 		name="terms"),
	url(r"^dmca/", 		static.dmca, 		name="dmca"),
	url(r"^privacy/", 	static.privacy, 	name="privacy"),
]
