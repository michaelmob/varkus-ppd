from channels import Group, auth


@auth.channel_session_user_from_http
def ws_connect(message):
	"""
	Add user's reply channel to Group on connection.
	"""
	message.reply_channel.send({"accept": True})
	message.channel_session["session_key"] = message.http_session.session_key
	session_key = message.channel_session["session_key"]
	Group("session-" + session_key).add(message.reply_channel)


@auth.channel_session_user
def ws_disconnect(message):
	"""
	Discard user's reply channel from Group after they have disconnected.
	"""
	session_key = message.channel_session["session_key"]
	Group("session-" + session_key).discard(message.reply_channel)