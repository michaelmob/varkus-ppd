def mock_offer(category, anchor, priority=False):
	"""
	Create mock offer dictionary.
	"""
	result = locals()
	result["requirements"] = "Requirements for " + result["anchor"]
	return result