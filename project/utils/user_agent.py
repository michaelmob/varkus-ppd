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
	
	else:
		return "Other"