from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import registration, account
from .models import Party


urlpatterns = [
	# Authentication
	url(r"^login/$",  auth_views.login, name="login"),
	url(r"^logout/$", auth_views.logout, {"template_name": "registration/logout.html"}, name="logout"),

	# User Registration
	url(r"^signup/$", registration.RegistrationView.as_view(), name="signup"),
	url(r"^signup/(?P<referrer>[0-9]+)/$", registration.RegistrationView.as_view(), name="signup-referral"),

	# Settings
	url(r"^account/$", account.AccountDetailView.as_view(), name="account"),
	url(r"^account/update/$", account.AccountUpdateView.as_view(), name="account-update"),

	# Password Resets
	url(r"^password_change/$", auth_views.password_change, {"template_name": "password/password_change.html"}, name="password_change"),
	url(r"^password_change/done/$", auth_views.password_change_done, {"template_name": "password/password_change_done.html"}, name="password_change_done"),
	url(r"^password_reset/$", auth_views.password_reset, {"template_name": "password/password_reset.html"}, name="password_reset"),
	url(r"^password_reset/done/$", auth_views.password_reset_done, {"template_name": "password/password_reset_done.html"}, name="password_reset_done"),
	url(r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", auth_views.password_reset_confirm, {"template_name": "password/password_reset_confirm.html"}, name="password_reset_confirm"),
	url(r"^reset/done/$", auth_views.password_change, {"template_name": "password/password_reset_complete.html"}, name="password_reset_complete")
]