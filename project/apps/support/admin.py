from django.contrib import admin
from . import models



@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	"""
	Admin for Contact Messages.
	"""
	list_display = ("name", "email", "subject", "ip_address", "datetime", "unread")
	list_filter = ("unread",)
	search_fields = ("name", "email", "ip_address")
	show_full_result_count = False



@admin.register(models.AbuseReport)
class AbuseReportAdmin(admin.ModelAdmin):
	"""
	Admin for Abuse Reports.
	"""
	list_display = ("name", "email", "complaint", "ip_address", "datetime", "unread")
	list_filter = ("unread",)
	search_fields = ("name", "email", "ip_address")
	show_full_result_count = False
