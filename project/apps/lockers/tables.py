import django_tables2 as tables

from apps.leads.models import Token, Lead
from apps.offers.tables import Table_Offer_Base


class Table_Locker_Lead(Table_Offer_Base):
	cut_amount = 1

	class Meta:
		orderable = True
		model = Lead
		empty_text = "This locker has not received any leads."
		attrs = {"class": "ui sortable table"}
		fields = ("offer", "user_ip_address", "user_payout", "date_time", "approved")

	def create(request, objects):
		table = __class__(objects)
		tables.RequestConfig(request, paginate={"per_page": 5}).configure(table)
		return table


class Table_Locker_Click(Table_Offer_Base):
	cut_amount = 1

	class Meta:
		orderable = True
		model = Token
		empty_text = "This locker has not received any clicks."
		attrs = {"class": "ui sortable table"}
		fields = ("ip_address", "last_access")

	def create(request, objects):
		table = __class__(objects)
		tables.RequestConfig(request, paginate={"per_page": 5}).configure(table)
		return table