from django.core.urlresolvers import reverse

from conversions.models import Token
from conversions.tables import ConversionsTableBase
from offers.tables import OfferTableBase, tables
from core.tables import TableBase, CurrencyColumn



class LockerTableBase(TableBase):
	"""
	Table to display locker objects.
	"""
	name = tables.LinkColumn(None, text=lambda r: r.name)
	conversions = tables.Column(accessor="earnings.conversions", verbose_name="Conversions")
	clicks = tables.Column(accessor="earnings.clicks", verbose_name="Clicks")
	earnings_month = CurrencyColumn(accessor="earnings.month", verbose_name="Month")
	earnings_total = CurrencyColumn(accessor="earnings.total", verbose_name="Total")


	class Meta(TableBase.Meta):
		model = None
		orderable = True
		empty_text = "You have not uploaded any files."
		prefix = "locker_"
		fields = (
			"name", "conversions", "clicks",
			"earnings_month", "earnings_total", "datetime"
		)



class LockerConversionsTable(ConversionsTableBase):
	"""
	Table to display conversions from a locker object.
	"""
	class Meta(ConversionsTableBase.Meta):
		empty_text = "This locker has not received any conversions."
		fields = ("offer", "ip_address", "payout", "datetime")
		exclude = ("approved", "ttc")
		prefix = "conversions-"



class LockerClicksTable(OfferTableBase):
	"""
	Table to display clicks from a locker object.
	"""
	class Meta(TableBase.Meta):
		orderable = True
		model = Token
		empty_text = "This locker has not received any clicks."
		fields = ("ip_address", "last_access")
		prefix = "clicks-"