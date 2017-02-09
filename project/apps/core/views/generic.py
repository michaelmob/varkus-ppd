from django_tables2 import SingleTableView
from ..forms import DateRangeForm



class DateRangeSingleTableView(SingleTableView):
	"""
	Base view for a SingleTableView with optional date range.
	"""
	date_range_form_class = DateRangeForm
	datetime_field = "datetime"


	def get_context_data(self, **kwargs):
		"""
		Add date range form to context data.
		Returns context dictionary.
		"""
		# Collect values from date range form class
		form = self.date_range_form_class(self.request.GET)
		self.date_range = form.get_date_range()

		# Add form to context
		context = super(__class__, self).get_context_data(**kwargs)
		context["date_range_form"] = form
		return context


	def get_table_data(self, **kwargs):
		"""
		Set date range on table data.
		Returns queryset.
		"""
		return super(__class__, self).get_table_data(**kwargs).filter(
			**{self.datetime_field + "__range": self.date_range}
		)