from django.core.cache import cache



class ActivityChart():
	"""
	Activity Chart
	"""
	def data(obj, **kwargs):
		"""
		Returns dictionary with clicks, conversions, and earnings for an hourly
		chart.
		"""
		# Chart template
		data = {x: [0, 0, 0] for x in range(24)}

		# Add clicks to first element of hour's element
		for o in obj.earnings.get_tokens_today(**kwargs).only("id"):
			data[o.datetime.hour][0] += 1

		# Add to the conversions and earnings of the hour's element
		for o in obj.earnings.get_conversions_today(**kwargs).only("payout"):
			data[o.datetime.hour][1] += 1
			data[o.datetime.hour][2] += float(o.payout)

		# Result {hour: (clicks, conversions, earnings) ...}
		return data


	def output(obj, **kwargs):
		"""
		Returns output data in dictionary.
		"""
		return {
			"success": True,
			"data": __class__.data(obj, **kwargs)
		}


	def output_cache(obj, **kwargs):
		"""
		Returns cached output or caches it if it's not already in cache.
		"""
		# Create key (line-chart-file.4)
		key = "line-chart-" + obj.__class__.__name__.lower() + "." + str(obj.pk)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = __class__.output(obj, **kwargs)
			cache.set(key, data, 60)

		return data



class MapChart():
	"""
	World Map Chart
	"""
	def data(obj, **kwargs):
		"""
		Returns dictionary with clicks, earnings, and conversions per country.
		"""
		# Chart template
		data = {}

		# Add to the conversions and earnings of the country's element
		for obj in obj.earnings.get_conversions_today(**kwargs).only("payout"):
			obj.country = obj.country.upper()

			# Try to add to 
			try:
				data[obj.country][0] += 1
				data[obj.country][1] += float(obj.payout)
			except:
				data[obj.country] = [1, float(obj.payout)]

		return data


	def output(obj):
		"""
		Returns output data in dictionary.
		"""
		return {
			"success": True,
			"data": MapChart.data(obj)
		}


	def output_cache(obj):
		"""
		Returns cached output or caches it if it's not already in cache.
		"""
		# Create key (map-chart-file.4)
		key = "map-chart-" + obj.__class__.__name__.lower() + "." + str(obj.pk)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = MapChart.output(obj)
			cache.set(key, data, 60)

		return data

