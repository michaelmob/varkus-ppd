"""
Viking 0.9.9
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

	# External Modules
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

	# Locker Modules
	"modules.widgets",
	"modules.lists",
	"modules.files",
	"modules.links",

)

MIDDLEWARE_CLASSES = (
	"django.middleware.cache.UpdateCacheMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"viking.middleware.cloudflare.CFMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.auth.middleware.SessionAuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"debug_toolbar.middleware.DebugToolbarMiddleware",
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
EMAIL_USE_SSL = True
EMAIL_HOST = "smtp"
EMAIL_PORT = 25


# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = ["*"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_SCHEME", "https")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "D33I>9XSio|zd4-wMy8S*TG0-3#8jgF,UEh47:a+4>_G3.+bv/{3Mb+0X<f}eEZz"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql_psycopg2",
		"HOST": os.environ.get("POSTGRES_HOST", "postgres"),
		"PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
		"NAME": os.environ.get("POSTGRES_DB", "postgres"),
		"USER": os.environ.get("POSTGRES_USER", "postgres"),
		"PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres")
	}
}


# Redis
REDIS_HOST = "redis://%s:%s/1" % (
	os.environ.get("REDIS_HOST", "redis"),
	os.environ.get("REDIS_PORT", "6379")
)


# Cache
# https://docs.djangoproject.com/en/dev/ref/settings/#cache
CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": REDIS_HOST,
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
        "CONFIG": {
            "hosts": [REDIS_HOST],
            "symmetric_encryption_keys": [SECRET_KEY],
        },
	},
}


# Media files (User Content)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static", "collection")

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


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

# Debug Toolbar
'''
if DEBUG:
	DEBUG_TOOLBAR_CONFIG = {
		"SHOW_TOOLBAR_CALLBACK": lambda r: True,
	}
'''

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
