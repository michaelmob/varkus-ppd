from .conversions import View_Conversions
from ..tables import Table_Statistics_Offers, Table_Statistics_Countries

class View_Statistics(View_Conversions):
	page = "month"
	title = "Statistics"
	table_icon = "bar graph"
	template = "conversions/statistics.html"


class View_Offers(View_Statistics):
	page = "offers"
	title = "Offer Statistics"
	table = Table_Statistics_Offers


class View_Countries(View_Statistics):
	page = "countries"
	title = "Country Statistics"
	table = Table_Statistics_Countries


class View_Chargebacks(View_Statistics):
	page = "chargebacks"
	title = "Chargeback Statistics"
