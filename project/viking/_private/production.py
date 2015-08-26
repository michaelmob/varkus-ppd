import os
from ..settings import BASE_DIR

SITE_NAME = "Viking"
SITE_DOMAIN = "viking.com"
SITE_URL = "https://" + SITE_DOMAIN

# SMTP
EMAIL_HOST = "localhost"
EMAIL_PORT = 25

# Admin
ADMINS = (
	("Owner", "me@viking.com"),
)


# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = [".viking.com", SITE_DOMAIN]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "################################################"


# Cache
# https://docs.djangoproject.com/en/1.8/ref/settings/#cache
CACHES = {
	"default": {
		"BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
		"LOCATION": "127.0.0.1:11211",
	}
}


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'viking',
		'USER': 'viking_user',
		'PASSWORD': 'viking_password',
		'HOST': 'localhost',
		'PORT': '3306',
	}
}


# Media files (User Content)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = ""  # os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "static/"),
)
