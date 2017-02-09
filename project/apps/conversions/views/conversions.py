from braces.views import LoginRequiredMixin

from core.views.generic import DateRangeSingleTableView
from ..models import Conversion
from ..tables import ConversionsTable



class ConversionsView(LoginRequiredMixin, DateRangeSingleTableView):
	model = Conversion
	table_class = ConversionsTable
	table_title = "Conversions"
	table_icon = "lightning"


	def get_context_data(self, **kwargs):
		"""
		Modify context data.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["table_title"] = self.table_title
		context["table_icon"] = self.table_icon
		return context


	def get_table_data(self, **kwargs):
		"""
		Filter for user's conversions.
		Returns queryset.
		"""
		return self.table_class.get_queryset({
			"user": self.request.user,
			self.datetime_field + "__range": self.date_range
		})