from decimal import Decimal

def keep_wanted(obj, wanted):
	result = {}

	for key, val in vars(obj).items():
		if key in wanted:
			if isinstance(val, Decimal):
				val = "%.2f" % val
			result[key] = val

	return result