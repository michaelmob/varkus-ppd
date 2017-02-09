# Site Info
SITE_NAME = "Viking"
SITE_DOMAIN = "viking.com"
SITE_URL = "https://" + SITE_DOMAIN

ALLOWED_HOSTS = ["." + SITE_DOMAIN, SITE_DOMAIN]

# Admins
ADMINS = (
	("Owner", "admin@" + SITE_DOMAIN),
)

# SMTP
SERVER_EMAIL = "error@" + SITE_DOMAIN
DEFAULT_FROM_EMAIL = "noreply@" + SITE_DOMAIN
EMAIL_HOST = "localhost"
EMAIL_PORT = 25

# Secret Key
SECRET_KEY = "################################################################"