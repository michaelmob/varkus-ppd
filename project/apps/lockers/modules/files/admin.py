from django.contrib import admin
from lockers.admin import ModelAdminMixin
from .models import File, FileEarnings



class FileEarningsInline(admin.StackedInline):
	"""
	Inline earnings for Files.
	"""
	model = FileEarnings



@admin.register(File)
class FileAdmin(ModelAdminMixin):
	"""
	Admin for File model.
	"""
	inlines = (FileEarningsInline,)
	list_display = (
		"name", "file_size", "user", "conversions", "earnings_today",
		"earnings_month", "earnings_total", "datetime"
	)