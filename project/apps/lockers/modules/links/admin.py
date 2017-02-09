from django.contrib import admin
from lockers.admin import ModelAdminMixin
from .models import Link, LinkEarnings



class LinkEarningsAdmin(admin.StackedInline):
	"""
	Inline earnings for Links.
	"""
	model = LinkEarnings



@admin.register(Link)
class LinkAdmin(ModelAdminMixin):
	"""
	Admin for Link model.
	"""
	inlines = (LinkEarningsAdmin,)