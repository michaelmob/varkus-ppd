from django.conf import settings
from django.contrib.auth.models import User
import django_tables2 as tables
from core.tables import TableBase



class ReferralTable(tables.Table):
	"""
	Table for a User's referred users.
	"""
	username = tables.Column(verbose_name="Username")
	date_joined = tables.Column(verbose_name="Date Joined")
	last_login = tables.Column(verbose_name="Last Login")


	class Meta(TableBase.Meta):
		model = User
		empty_text = "Looks like you haven't referred anyone."
		fields = ("username", "date_joined", "last_login")