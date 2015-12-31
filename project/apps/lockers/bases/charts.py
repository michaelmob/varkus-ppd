from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect

from apps.cp.bases.charts import Charts


class View_Line_Chart_Base(View):
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


class View_Map_Chart_Base(View):
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