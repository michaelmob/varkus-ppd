from collections import Counter
from django.core.cache import cache

class Charts():
	def line_data(obj, default=lambda: [{x: 0} for x in range(24)]):
		# Create chart template
		data1 = default()
		data2 = default()
		data3 = default()

		# Append small dictionary to chart list -- for clicks
		for token in obj.earnings.get_tokens_today():
			data1.append({token.date_time.hour: 1})

		# Append small dictionary to chart list -- for conversion count & earnings
		for conversion in obj.earnings.get_conversions_today():
			data2.append({conversion.date_time.hour: 1})
			data3.append({conversion.date_time.hour: float(conversion.user_payout)})

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

	def line_output(obj):
		clicks, conversions, earnings = Charts.line_data(obj)

		return {
			"success": True,
			"message": "",
			"data": [
				{"label": "Clicks", "data": clicks},
				{"label": "Conversions", "data": conversions},
				{"label": "Earnings", "data": earnings},
			]
		}

	def line_cache(obj):
		# Create key (lc_file_4)
		key = "lc_" + obj.__class__.__name__.lower() + str(obj.id)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = Charts.line_output(obj)
			cache.set(key, data, 60)

		return data

	def map_data(obj):
		result = []
		data = {}

		# Loop through conversions
		for obj in obj.earnings.get_conversions_today():
			obj.country = obj.country.upper()

			# If already exists just add onto the payment
			if obj.country in data:
				data[obj.country][0] += float(obj.user_payout)
				data[obj.country][1] += 1

			# Otherwise add the payment to the dict
			else:
				data[obj.country] = [float(obj.user_payout), 1]

		# Format to Google chart reqs
		for key, value in data.items():
			result.append((key, value[0], value[1]))

		return result

	def map_output(obj):
		return {
			"success": True,
			"message": "",
			"data": Charts.map_data(obj)
		}

	def map_cache(obj):
		# Create key (mc_file_4)
		key = "mc_" + obj.__class__.__name__.lower() + str(obj.id)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = Charts.map_output(obj)
			cache.set(key, data, 60)

		return data
