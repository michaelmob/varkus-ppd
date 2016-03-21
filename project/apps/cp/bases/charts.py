from collections import Counter
from django.core.cache import cache

from django.db.models import Count, Sum
from utils.database import is_sqlite

class Activity():
	def data(objs, fx=Count, field="id"):
		result = {x: 0 for x in range(24)}

		if is_sqlite():
			select = "strftime('%%H', date_time)"
		else:
			select = "extract(hour from date_time)"

		objs = objs \
			.extra(select={"hour": select}) \
			.values("hour").annotate(num=fx(field)) \
			.values_list("hour", "num")

		result.update({int(x): float(y) for x, y in objs})
		return list(result.items())

	def output(obj):
		queryset = obj.earnings.get_conversions_today()

		clicks = Activity.data(obj.earnings.get_tokens_today())
		conversions = Activity.data(queryset)
		earnings = Activity.data(queryset, Sum, "user_payout")

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
		# Create key (lc_file_4)
		key = "lc_" + obj.__class__.__name__.lower() + str(obj.id)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = Activity.output(obj)
			cache.set(key, data, 60)

		return data

class Map():
	def data(objs):
		results = objs.exclude(country=None).values("country") \
			.annotate(conversions=Count("id"), earnings=Sum("user_payout")) \
			.values_list("country", "conversions", "earnings")

		return [(result[0].upper(), int(result[1]), float(result[2])) \
			for result in results]

	def output(obj):
		return {
			"success": True,
			"message": "",
			"data": Map.data(obj.earnings.get_conversions_today())
		}

	def output_cache(obj):
		# Create key (mc_file_4)
		key = "mc_" + obj.__class__.__name__.lower() + str(obj.id)
		data = cache.get(key)

		# Cached does not exist, process and set
		if not data:
			data = Map.output(obj)
			cache.set(key, data, 60)

		return data
