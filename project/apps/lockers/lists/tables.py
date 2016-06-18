import django_tables2 as tables
from ..tables import Table_Locker_Base
from .models import List


class Table_List(Table_Locker_Base):
	earnings_conversions = tables.Column(accessor="earnings.conversions", verbose_name="Conversions")
	earnings_clicks = tables.Column(accessor="earnings.clicks", verbose_name="Clicks")
	earnings_month = tables.Column(accessor="earnings.month", verbose_name="Month")
	earnings_total = tables.Column(accessor="earnings.total", verbose_name="Total")
	
	class Meta(Table_Locker_Base.Meta):
		model = List
		empty_text = "You have not added any lists."
		fields = ("name", "item_count", "earnings_conversions", "earnings_clicks", "earnings_month", "earnings_total", "datetime")