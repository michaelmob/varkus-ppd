from django.contrib import admin
from lockers.admin import ModelAdminMixin
from .models import List, ListEarnings



class ListEarningsAdmin(admin.StackedInline):
	"""
	Inline earnings for Lists.
	"""
	model = ListEarnings



@admin.register(List)
class ListAdmin(ModelAdminMixin):
	"""
	Admin for List model.
	"""
	inlines = (ListEarningsAdmin,)