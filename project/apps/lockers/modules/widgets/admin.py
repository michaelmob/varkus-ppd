from django.contrib import admin
from lockers.admin import ModelAdminMixin
from .models import Widget, WidgetVisitor, WidgetEarnings



class WidgetEarningsInline(admin.StackedInline):
	"""
	Inline earnings for Widgets.
	"""
	model = WidgetEarnings



@admin.register(Widget)
class WidgetAdmin(ModelAdminMixin):
	"""
	Admin for Widget model.
	"""
	inlines = (WidgetEarningsInline,)



@admin.register(WidgetVisitor)
class WidgetVisitorAdmin(ModelAdminMixin):
	"""
	Admin for Widget Visitor model.
	"""
	list_display = ("id", "widget", "ip_address", "datetime")