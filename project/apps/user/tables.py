from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Count, F

import django_tables2 as tables
from utils.country import COUNTRIES

from apps.conversions.models import Conversion, Token
from apps.site.tables import Table_Base
from apps.offers.models import Offer
from apps.offers.tables import Table_Offer_Base

from utils.database import is_postgres, distinct_column

class Table_Referrals(tables.Table):
	username = tables.Column(verbose_name="Username")
	date_joined = tables.Column(verbose_name="Date Joined")
	last_login = tables.Column(verbose_name="Last Login")

	class Meta(Table_Base.Meta):
		model = User
		empty_text = "Looks like you haven't referred anyone."
		attrs = {"class": "ui sortable table"}
		fields = ("username", "date_joined", "last_login")

	def __init__(self, request, data=None, **kwargs):
		if not data:
			data = User.objects.filter(profile__referrer=request.user).order_by("-date_joined")

		super(__class__, self).__init__(data, **kwargs)
		tables.RequestConfig(request,
			paginate={"per_page": settings.ITEMS_PER_PAGE_MEDIUM}).configure(self)