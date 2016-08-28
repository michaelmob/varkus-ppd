from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views.signup import View_Sign_Up
from .views.account import View_Settings
from .models import Party

urlpatterns = [
	# Authentication
	url(r"^login/$",  login,  {"template_name": "user/login.html"},  name="login"),
	url(r"^logout/$", logout, {"template_name": "user/logout.html"}, name="logout"),

	# Account Creation
	url(r"^signup/$", View_Sign_Up.as_view(), name="signup"),
	url(r"^signup/(?P<referrer>[0-9]+)/$", View_Sign_Up.as_view(), name="signup-referral"),

	# Settings
	url(r"^account/settings/$", login_required(View_Settings.as_view()), name="account-settings"),
]

# Initiate default party, if it does not exist
Party.default()
