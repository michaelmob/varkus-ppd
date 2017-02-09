from django.views.generic.detail import DetailView
from braces.views import JSONResponseMixin

from ..charts import ActivityChart, MapChart


class ChartViewBase(JSONResponseMixin, DetailView):
	"""
	Base view for Charts.
	"""
	model = None


	def get_kwargs(self):
		"""
		Returns dictionary of kwargs to be used for chart lookup.
		"""
		return {}



class ActivityChartView(ChartViewBase):
	"""
	View for Activity Charts.
	"""
	def get(self, request, **kwargs):
		"""
		Returns JSON response of activity chart data.
		"""
		return self.render_json_response(
			ActivityChart.output_cache(self.get_object(), **self.get_kwargs())
		)



class MapChartView(ChartViewBase):
	"""
	View for Map Charts.
	"""
	def get(self, request, **kwargs):
		"""
		Returns JSON response of activity chart data.
		"""
		return self.render_json_response(
			MapChart.output_cache(self.get_object(), **self.get_kwargs())
		)