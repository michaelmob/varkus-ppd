from datetime import timedelta, date

from django.http import JsonResponse
from django.core.cache import cache


def line_chart_dict(objects, no_earnings=False):
	chart = []
	chart_dict = {x: [0.0, 0, 0] for x in range(24)}

	for obj in objects:
		key = (obj.date_time).hour

		if not no_earnings:
			# If already exists just add onto the payment
			if key in chart_dict:
				chart_dict[key][0] += float(obj.user_payout)

			# Otherwise add the payment to the dict
			else:
				chart_dict[key][0] = float(obj.user_payout)

		# Leads
		chart_dict[(obj.date_time).hour][1] += 1

		# Clicks
		#chart_dict[(obj.date_time).hour][2] += 1

	for key, value in chart_dict.items():
		chart.append((key, value[0], value[1], value[2]))

	return chart


def line_chart_array(objects):
	_dict = line_chart_dict(objects)

	chart = []

	for i in range(len(_dict[0])-1):
		chart.append([])

		for hour in _dict:
			chart[i].append([hour[0], hour[i+1]])

	return chart


def map_chart_dict(objects):
	chart = []
	chart_dict = {}

	for obj in objects:

		# If already exists just add onto the payment
		if obj.country in chart_dict:
			chart_dict[obj.country][0] += float(obj.user_payout)
			chart_dict[obj.country][1] += 1
		
		# Otherwise add the payment to the dict
		else:
			chart_dict[obj.country] = (float(obj.user_payout), 1)

	for key, value in chart_dict.items():
		chart.append((key, value[0], value[1]))

	return chart


def line_chart_view(key, func, no_earnings=False):
	data = cache.get(key)
	
	if (not data):
		objects = func()
		data = line_chart_array(objects)

		cache.set(key, data, 3600)

	return JsonResponse({
		"data": [
			{"label": "Clicks", "data": data[2]},
			{"label": "Leads", "data": data[1]},
			{"label": "Earnings", "data": data[0]} if not no_earnings else {},
		],
	})


def map_chart_view(key, func):
	data = cache.get(key)
	
	if (not data):
		objects = func()
		data = map_chart_dict(objects)

		cache.set(key, data, 3600)

	return JsonResponse({
		"data": data
	})
