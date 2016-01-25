WSGI_APPLICATION = "ws4redis.django_runserver.application"

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": "viking.db"
	}
}