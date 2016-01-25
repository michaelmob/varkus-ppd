def get_ua(user_agent):

	user_agent = user_agent.lower()

	if "windows" in user_agent:
		return "Windows"

	elif "android" in user_agent:
		return "Android"

	elif "iphone" in user_agent:
		return "iPhone"

	elif "ipad" in user_agent:
		return "iPad"

	elif "macintosh" in user_agent:
		return "Macintosh"

	elif "mobile" in user_agent:
		return "Mobile"

	elif "samsung" in user_agent:
		return "Samsung"

	else:
		return None


def format_ua(user_agent):
	if user_agent == "iphone":
		return "iPhone"

	if user_agent == "ipad":
		return "iPad"

	return user_agent.title()
