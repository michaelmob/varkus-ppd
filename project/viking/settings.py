"""
Viking 1.2.3

Django settings for Viking project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Quicksilver - Pride of Man

# TODO:
#######
# Use semantic ui api
# Widget example code
# Use polling to see active users on page
# Allow users to see IPs of visitors
# Referral guide

# Overwrite any setting in ./private/production.py for production servers
# Overwrite any setting in ./private/development.py for development servers

import os, socket
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = socket.gethostname() == "pc"

# Application definition

INSTALLED_APPS = (
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",

	"debug_toolbar", 		# django-debug-toolbar
	"captcha", 				# django-recaptcha
	"storages", 			# django-storages
	"axes", 				# django-axes
	"djcelery", 			# django-celery
	"anora", 				# anora
	"django_countries", 	# django-countries
	"django_gravatar",		# django-gravatar2
	"django_tables2", 		# django-tables2

	"apps.user",
	"apps.offers",
	"apps.cp",
	"apps.home",
	"apps.support",
	"apps.tickets",
	"apps.leads",
	"apps.billing",

	"apps.api",

	"apps.lockers",
	"apps.lockers.widgets",
	"apps.lockers.lists",
	"apps.lockers.files",
	"apps.lockers.links",
)

MIDDLEWARE_CLASSES = (
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.auth.middleware.SessionAuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"axes.middleware.FailedLoginMiddleware",
	"viking.middleware.cloudflare.CFMiddleware",
)

AUTHENTICATION_BACKENDS = (
	"viking.backends.auth.CaseInsensitiveModelBackend",
	"django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "viking.urls"

WSGI_APPLICATION = "viking.wsgi.application"

# Login
INVITE_ONLY = False
LOGIN_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/dashboard/"

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_L10N = False
USE_TZ = False

# Date Formatting
SHORT_DATETIME_FORMAT = "N j, Y, P"
DATETIME_FORMAT = "N j, Y, P"

SHORT_DATE_FORMAT = "N j, Y"
DATE_FORMAT = "N j, Y"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [
			os.path.join(BASE_DIR, "templates/")
		],
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
				"django.core.context_processors.request"
			],
			"loaders": [
				"django.template.loaders.filesystem.Loader",
				"django.template.loaders.app_directories.Loader",
			]
		},
	},
]

# SMTP
EMAIL_HOST = "localhost"
EMAIL_PORT = 25

# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "1pocfkh#z)llgp&h_t@svn^o3r^x6^g)s#qqx(udo0i7j3hj*e"

# Cache
# https://docs.djangoproject.com/en/1.9/ref/settings/#cache
CACHES = {
	"default": {
		"BACKEND": "django.core.cache.backends.locmem.LocMemCache",
		"LOCATION": "unique-snowflake"
	}
}

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": os.path.join(BASE_DIR, "db.sqlite3"),
	}
}

# Media files (User Content)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = ""  # os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static/"),
)

# Site Settings
SITE_NAME = "Development"
SITE_DOMAIN = "test.com"
SITE_URL = "https://" + SITE_DOMAIN

# GeoIP
GEOIP_PATH = "/home/dev/cb/project/geoip/"

# Add Site
from django.template.base import add_to_builtins
add_to_builtins("apps.home.templatetags.site")

# Gravatar
GRAVATAR_DEFAULT_IMAGE = "identicon"

# GeoIP
import geoip2.database
GEOIP = geoip2.database.Reader(os.path.join(BASE_DIR, "geoip/GeoLite2-City.mmdb"))

# E-mailing
SEND_EMAILS = True

# Axes
AXES_LOGIN_FAILURE_LIMIT = 10
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = timedelta(minutes=15)
AXES_LOCKOUT_TEMPLATE = "user/lockout.html"

# Storage
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Lockers Information
LOCKERS = (
	("WIDGET", "Widget"),
	("FILE", "File"),
	("LINK", "Link"),
	("LIST", "List"),
)

OFFERS_COUNT = 10

# Widgets Locker
MAX_WIDGETS = 10

# Files Locker
MAX_FILES = 10
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB

# Lists Locker
MAX_LISTS = 20

# Links Locker
MAX_LINKS = 20

# Reports
REPORT_MAX_FILE_SIZE = 4 * 1024 * 1024  # 4mb

# Default Party
DEFAULT_PARTY_ID = 1
DEFAULT_PARTY_NAME = "User"
DEFAULT_CUT_AMOUNT = 0.40  # Developers Cut
DEFAULT_REFERRAL_CUT_AMOUNT = 0.10

# Deposits # Default must exist // Always make "-1" default
DEPOSITS = (
	# User ID   Company     Aff ID      Deposit Code        Deposit Name        Password
	(-1,		"ADGATE",	43196,		"DEFAULT_DEPOSIT",	"Default Deposit",	"m20spl0h5jsjryfvg52s"),
	(1,			"ADGATE",	43196,		"MIKE_DEPOSIT",		"Mike's Deposit",	"54c1v40ivlc7usaumjwx"),
	(2,			"ADGATE",	2981,		"JOE_DEPOSIT",		"Joe's Deposit",	"jjbm086pcp2mdm00k5mf"),
)

DEPOSIT_NAMES = ((d[3], d[4],) for d in DEPOSITS)
POSTBACK_PASSWORD = DEPOSITS[0][5]
DEFAULT_AFFILIATE_ID = DEPOSITS[0][2]

CATEGORY_TYPES = (
	("Android", "Android"),
	("Downloads", "Downloads"),
	("Email Submits", "Email Submits"),
	("Free", "Free"),
	("Gifts", "Gifts"),
	("Hard Incentives", "Hard Incentives"),
	("Health & Beauty", "Health & Beauty"),
	("Home & Garden", "Home & Garden"),
	("iOS Devices", "iOS Devices"),
	("iPad", "iPad"),
	("iPhone", "iPhone"),
	("Lead Gen", "Lead Gen"),
	("Mobile WAP", "Mobile WAP"),
	("Online Services", "Online Services"),
	("PIN Submit", "PIN Submit"),
	("Samsung devices", "Samsung devices"),
	("Special Requests", "Special Requests"),
	("Surveys", "Surveys"),
	("", "")
)

CATEGORY_TYPES_ICONS = {
	"Android": "android",
	"Downloads": "download",
	"Email Submits": "mail outline",
	"Free": "certificate",
	"Gifts": "gift",
	"Hard Incentives": "bomb",
	"Health & Beauty": "female",
	"Home & Garden": "home",
	"iOS Devices": "apple",
	"iPad": "tablet",
	"iPhone": "mobile",
	"Lead Gen": "lightning",
	"Mobile WAP": "mobile",
	"Online Services": "desktop",
	"PIN Submit": "mobile",
	"Samsung devices": "mobile",
	"Special Requests": "checkered flag",
	"Surveys": "checkmark",
}

from .private._keys import *

if DEBUG:
	from .private.development import *
else:
	from .private.production import *
