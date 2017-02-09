def get_user_agent(user_agent):
	"""
	Return formatted and cleaned user-agent string.
	"""
	user_agent = user_agent.lower()

	if "windows" in user_agent:
		return "Windows"

	if "samsung" in user_agent:
		return "Samsung"

	if "android" in user_agent:
		return "Android"

	if "iphone" in user_agent:
		return "iPhone"

	if "ipad" in user_agent:
		return "iPad"

	if "macintosh" in user_agent:
		return "Macintosh"

	if "mobile" in user_agent:
		return "Mobile"

	if "linux" in user_agent:
		return "Linux"

	return None


def format_user_agent(user_agent):
	"""
	Returns formatted user-agent string.
	"""
	if user_agent == "iphone":
		return "iPhone"

	if user_agent == "ipad":
		return "iPad"

	return user_agent.title()


def user_agent_categories(user_agent):
	"""
	Return offer categories related to user-agent.
	"""
	if user_agent == "iPhone":
		return ["iPhone", "iOS Devices", "Mobile"]

	if user_agent == "iPad":
		return ["iPad", "iOS Devices", "Mobile"]

	if user_agent == "Windows":
		return ["Downloads"]

	if user_agent == "Samsung":
		return ["Android", "Samsung"]

	return [user_agent]