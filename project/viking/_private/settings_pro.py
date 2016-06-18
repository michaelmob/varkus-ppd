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
	("Owner", "admin@viking.com"),
)

SERVER_EMAIL = "error@viking.com"
DEFAULT_FROM_EMAIL = "noreply@viking.com"

# SECURITY WARNING: do not run with debug turned on in production!
ALLOWED_HOSTS = [".viking.com", SITE_DOMAIN]