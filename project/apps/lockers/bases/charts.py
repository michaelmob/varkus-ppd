from collections import Counter

from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.cache import cache


class Charts():
	def line(obj, default=lambda: [{x: 0} for x in range(24)]):
		# Create chart template
		data1 = default()
		data2 = default()
		data3 = default()

		# Append small dictionary to chart list -- for clicks
		for token in obj.earnings.get_tokens():
			data1.append({token.date_time.hour: 1})

		# Append small dictionary to chart list -- for lead count & earnings
		for lead in obj.earnings.get_leads():
			data2.append({lead.date_time.hour: 1})
			data3.append({lead.date_time.hour: float(lead.user_payout)})

		# Merge duplicate keyed arrays -- for clicks
		counter1 = Counter()
		for hour in data1: counter1.update(hour)

		# Merge duplicate keyed arrays -- for lead count
		counter2 = Counter()
		for hour in data2: counter2.update(hour)

		# Merge duplicate keyed arrays -- for earnings
		counter3 = Counter()
		for hour in data3: counter3.update(hour)

		# Result (clicks, leads, earnings)
		return (list(counter1.items()), list(counter2.items()), list(counter3.items()))

	def line_cache(obj):
		# Create key (lc_file_4)
		key = "lc_" + obj.__class__.__name__ + str(obj.id)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			clicks, leads, earnings = Charts.line(obj)

			data = {
				"data": [
					{"label": "Clicks", "data": clicks},
					{"label": "Leads", "data": leads},
					{"label": "Earnings", "data": earnings},
				],
			}
	
			cache.set(key, data, 3600)

		return data

	def map(obj):
		result = []
		data = {}

		# Loop through leads
		for obj in obj.earnings.get_leads():
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

	def map_cache(obj):
		# Create key (mc_file_4)
		key = "mc_" + obj.__class__.__name__ + str(obj.id)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = Charts.map(obj)
	
			cache.set(key, data, 3600)

		return {"data": data}


class View_Line_Chart(View):
	model = None

	def obj(self, request, code):
		# Redirect to overview if no code provided
		if not code:
			return None

		# Get object, otherwise redirect to overview
		try:
			return self.model.objects.get(user=request.user, code=code)
		except self.model.DoesNotExist:
			return None

	def get(self, request, code=None):
		obj = self.obj(request, code)
		
		# Redirect if not existant
		if not obj:
			return JsonResponse({})

		# Get line data from cache, if exists
		data = Charts.line_cache(obj)
		return JsonResponse(data)


class View_Map_Chart(View):
	model = None

	def obj(self, request, code):
		# Redirect to overview if no code provided
		if not code:
			return None

		# Get object, otherwise redirect to overview
		try:
			return self.model.objects.get(user=request.user, code=code)
		except self.model.DoesNotExist:
			return None

	def get(self, request, code=None):
		obj = self.obj(request, code)
		
		# Redirect if not existant
		if not obj:
			return JsonResponse({})

		# Get line data from cache, if exists
		data = Charts.map_cache(obj)
		return JsonResponse(data)