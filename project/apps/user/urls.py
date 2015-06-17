from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth.views import (
	login, logout, password_reset, password_reset_done,
	password_reset_confirm, password_reset_complete,
	password_change, password_change_done
)
from .views.signup import signup
from .views.user_settings import user_settings
from .models import Party

urlpatterns = [
	url(r"^login/", login, {"template_name": "user/login.html"}, name="login"),
	url(r"^logout/", logout, {"template_name": "user/logout.html"}, name="logout"),
	url(r"^signup/$", signup, name="signup"),
	url(r"^signup/(?P<referrer>[0-9]+)", signup, name="signup-referral"),

	# Settings
	url(r"^settings/$", user_settings, name="user-settings"),
	url(r"^settings/(?P<save>\w+)", user_settings, name="user-settings-modify"),

	# Password Reset
	url(
		r"^change-password/$",
		password_change,
		{"template_name": "user/password-change/change.html"},
		name="password-change"
	),

	url(
		r"^change-password/done/$",
		password_change_done,
		{"template_name": "user/password-change/done.html"},
		name="password_change_done"
	),

	# Password Reset
	url(
		r"^password-reset/$",
		password_reset,
		{"template_name": "user/password-reset/reset.html"},
		name="password-reset"
	),

	url(
		r"^password-reset/done/$",
		password_reset_done,
		{"template_name": "user/password-reset/done.html"},
		name="password_reset_done"
	),
	
	url(
		r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
		password_reset_confirm,
		{"template_name": "user/password-reset/confirm.html"},
		name="password_reset_confirm"
	),

	url(
		r"^password-reset/complete/$",
		password_reset_complete,
		{"template_name": "user/password-reset/complete.html"},
		name="password_reset_complete"
	),
]


# Create Default Party
__default_party_check = False

if not __default_party_check:
	from django.conf import settings
	
	__party, __created = Party.objects.get_or_create(
		name=settings.DEFAULT_PARTY_NAME,
		defaults={
			"cut_amount": settings.DEFAULT_CUT_AMOUNT,
			"referral_cut_amount": settings.DEFAULT_REFERRAL_CUT_AMOUNT
		}
	)
	
	__default_party_check = True

user_count = User.objects.all().count()