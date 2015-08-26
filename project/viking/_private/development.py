import os
from ..settings import BASE_DIR

SITE_NAME = "Development"
SITE_DOMAIN = "test.com"
SITE_URL = "https://" + SITE_DOMAIN

# SMTP
EMAIL_HOST = "localhost"
EMAIL_PORT = 25


# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = []


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "1pocfkh#z)llgp&h_t@svn^o3r^x6^g)s#qqx(udo0i7j3hj*e"

# Cache
# https://docs.djangoproject.com/en/1.8/ref/settings/#cache
CACHES = {
	"default": {
		"BACKEND": "django.core.cache.backends.locmem.LocMemCache",
		"LOCATION": "unique-snowflake"
	}
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
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
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = ""  # os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static/"),
)
