import django_tables2 as tables

from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


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