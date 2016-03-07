from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

import django_tables2 as tables
from utils.country import COUNTRIES

from apps.conversions.models import Conversion, Token
from apps.offers.models import Offer
from apps.offers.tables import Table_Offer_Base

from utils.database import is_postgres, distinct_column

class Table_Referrals(tables.Table):
	username = tables.Column(verbose_name="Username")
	date_joined = tables.Column(verbose_name="Date Joined")
	last_login = tables.Column(verbose_name="Last Login")

	class Meta:
		model = User
		empty_text = "Looks like you haven't referred anyone."
		attrs = {"class": "ui sortable table"}
		fields = ("username", "date_joined", "last_login")

	def create(request):
		table = __class__(User.objects.filter(profile__referrer=request.user).order_by("-date_joined"))
		tables.RequestConfig(request, paginate={"per_page": 10}).configure(table)
		return table


class Table_Statistics_Base(Table_Offer_Base):

	class Meta:
		model = Conversion
		orderable = True
		empty_text = "There doesn't seem to be any conversions here for this category or date range."
		attrs = {"class": "ui sortable table"}
		fields = ("clicks", "conversions")

	def __init__(self, field, request, date_range=None):
		# Filter Args
		self.field = field
		self.cut_amount = request.user.profile.party.cut_amount
		self.args = {"user": request.user}
		if date_range != None and date_range[0] != None:
			self.args["date_time__range"] = date_range

		# Distinct only works in Postgres
		if is_postgres():
			data = Conversion.objects.filter(**self.args).distinct(field)
		else:
			data = distinct_column(Conversion.objects.filter(**self.args), field)

		# Create Table
		super(__class__, self).__init__(data)
		tables.RequestConfig(request, paginate={"per_page": 30}).configure(self)

	def _render_(self, model, record, extra=None):
		args = self.args.copy()
		args.update({self.field: eval("record." + self.field)})
		if extra:
			args.update(extra)
		return model.objects.filter(**args).count()

	def render_clicks(self, record):
		return self._render_(Token, record)

	def render_conversions(self, record):
		return self._render_(Conversion, record)

	def render_chargebacks(self, record):
		return self._render_(Conversion, record, {"approved": False})


class Table_Statistics_Offers(Table_Statistics_Base):
	clicks = tables.Column(empty_values=(), orderable=False)
	conversions = tables.Column(empty_values=(), orderable=False)
	chargebacks = tables.Column(empty_values=(), orderable=False)

	class Meta(Table_Statistics_Base.Meta):
		fields = ("offer", "clicks", "conversions", "user_payout", "chargebacks")

	def __init__(self, request, date_range=None):
		super(__class__, self).__init__("offer", request, date_range)

	def render_clicks(self, record):
		return Token.objects.filter(offers__in=[record.offer], **self.args).count()


class Table_Statistics_Countries(Table_Statistics_Base):
	clicks = tables.Column(empty_values=(), orderable=False)
	conversions = tables.Column(empty_values=(), orderable=False)
	chargebacks = tables.Column(empty_values=(), orderable=False)

	class Meta(Table_Statistics_Base.Meta):
		fields = ("country", "clicks", "conversions")

	def __init__(self, request, date_range=None):
		super(__class__, self).__init__("country", request, date_range)

	def render_country(self, value):
		return mark_safe("<i class='%s flag'></i>%s" % (value.lower(), COUNTRIES[value.upper()]))