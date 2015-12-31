import os
os.environ.update(DJANGO_SETTINGS_MODULE="viking.settings")

import gevent.socket
import redis.connection
redis.connection.socket = gevent.socket

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()