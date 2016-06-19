"""
Viking 0.5.0
"""

# Overwrite any setting in ./private/settings_production.py for production servers
# Overwrite any setting in ./private/settings_development.py for development servers

import os, socket
from datetime import timedelta

# Debug
# https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-DEBUG
DEBUG = os.environ.get("DEBUG", "").lower() == "true"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition
INSTALLED_APPS = (
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.postgres",

	"debug_toolbar",        # django-debug-toolbar
	"captcha",              # django-recaptcha
	"storages",             # django-storages
	"axes",                 # django-axes
	"djcelery",             # django-celery
	"anora",                # anora
	"django_countries",     # django-countries
	"django_gravatar",      # django-gravatar2
	"django_tables2",       # django-tables2
	"channels",             # channels

	"apps.user",
	"apps.offers",
	"apps.cp",
	"apps.site",
	"apps.support",
	"apps.tickets",
	"apps.conversions",
	"apps.billing",
	"apps.api",
	"apps.lockers",
	"apps.lockers.widgets",
	"apps.lockers.lists",
	"apps.lockers.files",
	"apps.lockers.links",
)

MIDDLEWARE_CLASSES = (
	"django.middleware.cache.UpdateCacheMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.auth.middleware.SessionAuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"axes.middleware.FailedLoginMiddleware",
	"viking.middleware.cloudflare.CFMiddleware",
	"viking.middleware.session_verify.SessionVerifyMiddleware",
)

AUTHENTICATION_BACKENDS = (
	"viking.backends.auth.CaseInsensitiveModelBackend",
	"django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "viking.urls"

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
				"django.template.context_processors.request",
			],
			"loaders": [
				"django.template.loaders.filesystem.Loader",
				"django.template.loaders.app_directories.Loader",
			],
			"builtins": ["apps.site.templatetags.site"],
		},
	},
]

# SMTP
EMAIL_HOST = "localhost"
EMAIL_PORT = 25

# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = []
SECURE_PROXY_SSL_HEADER = ("HTTP_X_SCHEME", "https")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql_psycopg2",
		"HOST": os.environ["DB_HOST"],
		"PORT": os.environ["DB_PORT"],
		"NAME": os.environ["DB_NAME"],
		"USER": os.environ["DB_USER"],
		"PASSWORD": os.environ["DB_PASS"],
	}
}

# Cache
# https://docs.djangoproject.com/en/dev/ref/settings/#cache
CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://%s:%s/1" % (
			os.environ.get("REDISHOST", "127.0.0.1"),
			os.environ.get("REDISPORT", "6379")),
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		}
	}
}

# Session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Channels
CHANNEL_LAYERS = {
	"default": {
		"BACKEND": "asgi_redis.RedisChannelLayer",
		"ROUTING": "viking.routing.channel_routing",
	},
}

# Media files (User Content)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media/")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR

STATICFILES_DIRS = (
	os.path.join("..", "static/"),
)

# Site Settings
SITE_NAME = os.environ.get("SITE_NAME", "Viking")
SITE_DOMAIN = os.environ.get("DOMAIN", "viking.com")
SITE_URL = "https://" + SITE_DOMAIN

MESSAGE_TAGS = {
	10: "orange", 20: "blue", 25: "green", 30: "warning", 40: "red", 50: "red"
}

# Gravatar
GRAVATAR_DEFAULT_IMAGE = "identicon"

# GeoIP
GEOIP_PATH = BASE_DIR

# HTTP Notification Proxy
HTTP_NOTIFICATION_USE_PROXY = False
SOCKS5_SERVER = ""
SOCKS5_PORT = 1080
SOCKS5_USERNAME = None
SOCKS5_PASSWORD = None

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

LOCKER_THEMES = (
	("DEFAULT", "Default"),
	("BLANK", "Blank"),
)

# Tables
ITEMS_PER_PAGE_LARGE = 20
ITEMS_PER_PAGE_MEDIUM = 10
ITEMS_PER_PAGE_SMALL = 5

# Offers
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

# Deposits // Default must exist // Always make "-1" default
DEPOSITS = (
	# User ID   Company         Aff ID  Deposit Code        Deposit Name        Password
	(-1,        "ADGATEMEDIA",  1,      "DEFAULT_DEPOSIT",  "Default Deposit",  "PASSWORD"),
)

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
	("Conversion Gen", "Conversion Gen"),
	("Mobile Subscription", "Mobile Subscription"),
	("Mobile WAP", "Mobile WAP"),
	("Online Services", "Online Services"),
	("PIN Submit", "PIN Submit"),
	("Samsung devices", "Samsung devices"),
	("Special Requests", "Special Requests"),
	("Surveys", "Surveys"),
	("", "")
)

CATEGORY_TYPES_ICONS = {
	"Android" 				: "android",
	"Downloads"				: "download",
	"Email Submits"			: "mail outline",
	"Free"					: "certificate",
	"Gifts"					: "gift",
	"Hard Incentives"		: "bomb",
	"Health & Beauty"		: "female",
	"Home & Garden"			: "home",
	"iOS Devices"			: "apple",
	"iPad"					: "tablet",
	"iPhone"				: "mobile",
	"Conversion Gen"		: "lightning",
	"Mobile Subscription"	: "mobile",
	"Mobile WAP"			: "mobile",
	"Mobile Content"		: "mobile",
	"Online Services"		: "desktop",
	"PIN Submit"			: "mobile",
	"Samsung devices"		: "mobile",
	"Special Requests"		: "checkered flag",
	"Surveys"				: "checkmark",
}

from .private.keys import *
from .private.settings_common import *

if DEBUG:
	from .private.settings_development import *
else:
	from .private.settings_production import *
