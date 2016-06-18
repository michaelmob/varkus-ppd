from collections import Counter
from django.core.cache import cache

class Activity():
	def data(obj, default=lambda: [{x: 0} for x in range(24)]):
		# Create chart template
		data1 = default()
		data2 = default()
		data3 = default()

		# Append small dictionary to chart list -- for clicks
		for token in obj.earnings.get_tokens_today():
			data1.append({token.datetime.hour: 1})

		# Append small dictionary to chart list -- for conversion count & earnings
		for conversion in obj.earnings.get_conversions_today():
			data2.append({conversion.datetime.hour: 1})
			data3.append({conversion.datetime.hour: float(conversion.user_payout)})

		# Merge duplicate keyed arrays -- for clicks
		counter1 = Counter()
		for hour in data1: counter1.update(hour)

		# Merge duplicate keyed arrays -- for conversion count
		counter2 = Counter()
		for hour in data2: counter2.update(hour)

		# Merge duplicate keyed arrays -- for earnings
		counter3 = Counter()
		for hour in data3: counter3.update(hour)

		# Result (clicks, conversions, earnings)
		return (list(counter1.items()), list(counter2.items()), list(counter3.items()))

	def output(obj):
		clicks, conversions, earnings = Activity.data(obj)

		return {
			"success": True,
			"message": "",
			"data": [
				{"label": "Clicks", "data": clicks},
				{"label": "Conversions", "data": conversions},
				{"label": "Earnings", "data": earnings},
			]
		}

	def output_cache(obj):
		# CCreate key (line-chart:file.4)
		key = "line-chart:" + obj.__class__.__name__.lower() + "." + str(obj.pk)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = Activity.output(obj)
			cache.set(key, data, 60)

		return data


class Map():
	def data(obj):
		result = []
		data = {}

		# Loop through conversions
		for obj in obj.earnings.get_conversions_today():
			obj.country = obj.country.upper()

			# If already exists just add onto the payment
			if obj.country in data:
				data[obj.country][0] += 1
				data[obj.country][1] += float(obj.user_payout)

			# Otherwise add the payment to the dict
			else:
				data[obj.country] = [1, float(obj.user_payout)]

		# Format to Google chart reqs
		for key, value in data.items():
			result.append((key, value[0], value[1]))

		return result

	def output(obj):
		return {
			"success": True,
			"message": "",
			"data": Map.data(obj)
		}

	def output_cache(obj):
		# Create key (map-chart:file.4)
		key = "map-chart:" + obj.__class__.__name__.lower() + "." + str(obj.pk)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = Map.output(obj)
			cache.set(key, data, 60)

		return data

