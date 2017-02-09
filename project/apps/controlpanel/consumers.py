from channels import Group, auth


@auth.channel_session_user_from_http
def ws_connect(message):
	"""
	Add user's reply channel to Group on connection.
	"""
	message.reply_channel.send({"accept": True})
	message.channel_session["session_key"] = message.http_session.session_key
	Group("broadcast").add(message.reply_channel)
	Group("user-" + str(message.user.pk)).add(message.reply_channel)


@auth.channel_session_user
def ws_disconnect(message):
	"""
	Discard user's reply channel from Group after they have disconnected.
	"""
	Group("broadcast").discard(message.reply_channel)
	Group("user-" + str(message.user.pk)).discard(message.reply_channel)