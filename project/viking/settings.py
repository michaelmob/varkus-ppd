"""
Viking 0.9.12
"""

# Override any setting in ./private/settings_production.py for production servers
# Override any setting in ./private/settings_development.py for development servers

import os
import sys
from datetime import timedelta


# Debug
# https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-DEBUG
DEBUG = os.environ.get("DEBUG", False)
INTERNAL_IPS = ["172.18.0.1", "192.168.0.1"]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
sys.path.insert(0, os.path.join(BASE_DIR, "apps/lockers"))


# Application definition
INSTALLED_APPS = (
	# Django contributions
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.postgres",

	# External modules
	"dbbackup",					# django-dbbackup
	"debug_toolbar",			# django-debug-toolbar
	"captcha",					# django-recaptcha
	"storages",					# django-storages
	"axes",						# django-axes
	"anora",					# anora
	"django_countries",			# django-countries
	"django_gravatar",			# django-gravatar2
	"django_tables2",			# django-tables2
	"channels",					# channels
	"semanticuiforms", 			# semanticuiforms
	"django_celery_results",	# django-celery-results

	# Apps
	"core",
	"staff",
	"users",
	"controlpanel",
	"offers",
	"support",
	"billing",
	"tickets",
	"conversions",
	"lockers",

	# Locker modules
	"modules.widgets",
	"modules.lists",
	"modules.files",
	"modules.links",
)

MIDDLEWARE = (
	#"viking.middleware.cloudflare.CFMiddleware",
	"debug_toolbar.middleware.DebugToolbarMiddleware",
	"django.middleware.cache.UpdateCacheMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
)

AUTHENTICATION_BACKENDS = (
	"viking.backends.auth.CaseInsensitiveModelBackend",
	"django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "viking.urls"

TEST_RUNNER = "viking.runners.testrunner.TestRunner"


# Login
INVITE_ONLY = False
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
TIME_ZONE = "America/New_York"


# Date Formatting
SHORT_DATETIME_FORMAT = "N j, Y, P"
DATETIME_FORMAT = "N j, Y, P"

SHORT_DATE_FORMAT = "N j, Y"
DATE_FORMAT = "N j, Y"


# Templates
TEMPLATES = [{
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
			"django.template.context_processors.request",
		],
		"loaders": [
			"django.template.loaders.filesystem.Loader",
			"django.template.loaders.app_directories.Loader",
		],
		"builtins": ["core.templatetags.site"],
	},
}]


# SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp"
EMAIL_PORT = 25


# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = ["*"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_SCHEME", "https")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql_psycopg2",
		"HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
		"PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
		"NAME": os.environ.get("POSTGRES_DB"),
		"USER": os.environ.get("POSTGRES_USER"),
		"PASSWORD": os.environ.get("POSTGRES_PASSWORD")
	}
}

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "/var/backups"}
DBBACKUP_CLEANUP_KEEP = 5
DBBACKUP_CLEANUP_KEEP_MEDIA = 2


# Cache
# https://docs.djangoproject.com/en/dev/ref/settings/#cache
CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/1",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	}
}


# Channels
CHANNEL_LAYERS = {
	"default": {
		"BACKEND": "asgi_redis.RedisChannelLayer",
		"ROUTING": "viking.routing.channel_routing",
	},
}


# Media files (User Content)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = ()


# Site Settings
SITE_NAME = os.environ.get("SITE_NAME", "Viking")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "viking.com")
SITE_URL = "https://" + SITE_DOMAIN

MESSAGE_TAGS = {
	10: "orange", 20: "blue", 25: "green", 30: "warning", 40: "red", 50: "red"
}


# Gravatar
GRAVATAR_DEFAULT_IMAGE = "identicon"


# GeoIP
GEOIP_PATH = "/var/"


# Proxies
USE_PROXY = True
PROXY_SERVER = ("proxy-nl.privateinternetaccess.com", 1080)
PROXY_CREDENTIALS = {
	"username": "x2927670",
	"password": "pWCSn2ep4H"
}


# E-mailing
SEND_EMAILS = True


# Axes
AXES_LOGIN_FAILURE_LIMIT = 10
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = timedelta(minutes=15)
AXES_LOCKOUT_TEMPLATE = "user/lockout.html"


# Storage
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


# Lockers Information
LOCKERS = (
	("WIDGET", "Widget"),
	("FILE", "File"),
	("LINK", "Link"),
	("LIST", "List"),
)

LOCKER_ICONS = {
	"WIDGET": "file image outline",
	"FILE": "file text",
	"LINK": "linkify",
	"LIST": "list layout",
}

LOCKER_THEMES = (
	("DEFAULT", "Default"),
	("BLANK", "Blank"),
)


# Tables
ITEMS_PER_PAGE_LARGE = 20
ITEMS_PER_PAGE_MEDIUM = 10
ITEMS_PER_PAGE_SMALL = 5


# Offers
OFFER_COUNT = 10
OFFER_CACHE_TIME = 5 * 60  # 5 minutes
OFFER_DISPLAY = {
	"User Agent": .30,
	"Email Submits": .30,
	"PIN Submit": .20,
}


# Widgets Locker
MAX_WIDGETS = 10
VIRAL_MESSAGE = "Send the link below to {amount} more {noun} to continue."
CSS_MAX_FILE_SIZE = 1 * 1024 * 1024  # 1mb


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


# Deposits // Default must exist // Always make "-1" default
DEPOSITS = (
	# User ID   Company         Aff ID  Deposit Code        Deposit Name        Password
	(-1,        "ADGATEMEDIA",  1,      "DEFAULT_DEPOSIT",  "Default Deposit",  "PASSWORD"),
)


from .private.settings_common import *


if DEBUG:
	from .private.settings_development import *
else:
	from .private.settings_production import *
