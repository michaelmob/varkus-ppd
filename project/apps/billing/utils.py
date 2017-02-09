from datetime import date, timedelta


def net_days(date_, days):
	"""
	Returns date with days added.
	"""
	return date_ + timedelta(days=days)


def month_range(date_):
	"""
	Return tuple consisting of first of month and last of month.
	"""
	year = date_.year
	month = date_.month + 1

	if month > 12:
		month = 1
		year += 1

	return (date(date_.year, date_.month, 1), date(year, month, 1))