"""
Siren 1.0.2

Django settings for Siren project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# apt-get install
#	build-essential
#	python3.4-dev
#	python-magic
#	rabbitmq-server

# pip install
#   django
#   django-recaptcha
#   django-storages
#   django-axes
#   django-celery
#   pillow
#   django-countries
#   anora


# The Green Roots - Wait a Million Years
# The Green Roots - Sooner or Later
# Quicksilver - Pride of Man
# 3 Dog Night - Joy to The world
# Michael Bruce - So Far So Good

# TODO:
#######
# Front Page /// 0%
# Widgets along with example code // 50%
# Postbacks /// 80%
# Postbacks Page telling user to create postback with widget /// 50%
# Tickets unread variable and badge on icon /// 0%
# Staff section rework /// 0%
# -- Leads
# -- Deposits
# -- Tickets
# Fix maps /// 0%
# In all lockers rename variable "item" to "obj" /// 100%

import os, socket
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: don"t run with debug turned on in production! 
DEBUG = socket.gethostname() == "pc"

if DEBUG:
	from .private.development import *
else:
	from .private.production import *

# Application definition

INSTALLED_APPS = (
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",

	"captcha",              # django-recaptcha
	"storages",             # django-storages
	"axes",                 # django-axes
	"djcelery",             # django-celery
	"anora",                # anora
	"django_countries",     # django-countries

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
	"siren.middleware.cloudflare.CFMiddleware",
)

AUTHENTICATION_BACKENDS = (
	"siren.backends.auth.CaseInsensitiveModelBackend",
	"django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "siren.urls"

WSGI_APPLICATION = "siren.wsgi.application"

# Cache
CACHES = {
	"default": {
		"BACKEND": "django.core.cache.backends.locmem.LocMemCache",
		"LOCATION": "unique-snowflake"
	}
}

# Login
LOGIN_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/dashboard/"

# GeoIP
GEOIP_PATH = "/home/dev/cb/project/geoip/"

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = False

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

# Add Site
from django.template.base import add_to_builtins
add_to_builtins("apps.home.templatetags.site")

INVITE_ONLY = True

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
DEFAULT_CUT_AMOUNT = 0.30  # Developers Cut
DEFAULT_REFERRAL_CUT_AMOUNT = 0.10

# Adgate
OFFER_REDIRECT_URL = "http://2.quicktrkr.com/cl/%s/%s?s1=%s"

# Deposits # Default must exist // Always make "-1" default
DEPOSITS = (
	# User ID   Company     Aff ID      Deposit Code        Deposit Name        Password
	(-1,        "ADGATE",   43196,       "DEFAULT_DEPOSIT",  "Default Deposit",  "m20spl0h5jsjryfvg52s"),
	(1,         "ADGATE",   43196,       "MIKE_DEPOSIT",     "Mike's Deposit",   "54c1v40ivlc7usaumjwx"),
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
	"iPhone": "phone",
	"Lead Gen": "lightning",
	"Mobile WAP": "mobile",
	"Online Services": "desktop",
	"PIN Submit": "mobile",
	"Samsung devices": "mobile",
	"Special Requests": "checkered flag",
	"Surveys": "checkmark",
}

from .private._keys import *
