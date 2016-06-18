import django_tables2 as tables

from apps.conversions.models import Conversion
from apps.offers.models import Offer
from apps.offers.tables import Table_Offer_Base, Table_Offer_Conversions


class Table_Offer(Table_Offer_Base):
	name = tables.Column(accessor="name")

	class Meta(Table_Offer_Base.Meta):
		orderable = False
		model = Offer
		attrs = {"class": "ui table"}
		fields = ("name", "flag", "earnings_per_click", "payout")


class Table_Conversions(Table_Offer_Conversions):
	class Meta(Table_Offer_Conversions.Meta):
		model = Conversion
		orderable = False
		empty_text = "You haven't received any conversions, yet."