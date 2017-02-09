from .conversions import ConversionsView
from ..tables import OfferStatisticsTable, CountryStatisticsTable



class StatisticsViewBase(ConversionsView):
	"""
	Base statistics view.
	"""
	table_icon = "bar graph"
	template_name = "conversions/statistic_list.html"


	def get_context_data(self, **kwargs):
		"""
		Add 'category' element to context dictionary.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["category"] = self.category
		return context



class OffersView(StatisticsViewBase):
	"""
	Statistics view for offers.
	"""
	category = "offers"
	table_title = "Offer Statistics"
	table_class = OfferStatisticsTable



class CountriesView(StatisticsViewBase):
	"""
	Statistics view for countries.
	"""
	category = "countries"
	table_title = "Country Statistics"
	table_class = CountryStatisticsTable