import django_tables2 as tables
from ..tables import Table_Locker_Base
from .models import Widget


class Table_Widget(Table_Locker_Base):
	earnings_conversions = tables.Column(accessor="earnings.conversions", verbose_name="Conversions")
	earnings_clicks = tables.Column(accessor="earnings.clicks", verbose_name="Clicks")
	earnings_month = tables.Column(accessor="earnings.month", verbose_name="Month")
	earnings_total = tables.Column(accessor="earnings.total", verbose_name="Total")
	
	class Meta(Table_Locker_Base.Meta):
		model = Widget
		empty_text = "You have not created any widgets."