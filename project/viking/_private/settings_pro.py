import os
from ..settings import BASE_DIR

# Site Info
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

# E-mail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False

SERVER_EMAIL = "error@viking.com"
DEFAULT_FROM_EMAIL = "noreply@viking.com"

# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = [".viking.com", SITE_DOMAIN]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "################################################"

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


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql_psycopg2",
		"NAME": "viking",
		"USER": "username",
		"PASSWORD": "password",
		"HOST": "127.0.0.1",
		"PORT": "5432",
	}
}