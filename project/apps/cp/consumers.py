from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
	message.channel_session["session_key"] = message.http_session.session_key
	Group("user-" + str(message.user.pk)).add(message.reply_channel)

# Disconnected from websocket.disconnect
@channel_session_user
def ws_disconnect(message):
	Group("user-" + str(message.user.pk)).discard(message.reply_channel)