from django.core.cache import cache as c


def get(key, func, timeout=3600):
	result = c.get(key)

	if (not result):
		result = func()
		c.set(key, result, timeout)

	return result
