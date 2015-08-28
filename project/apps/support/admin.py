from django.contrib import admin
from apps.support.models import Contact_Message, Abuse_Report


@admin.register(Contact_Message)
class Admin_Contact_Message(admin.ModelAdmin):
	list_display = ("name", "email", "user", "subject", "ip_address", "date_time", "viewed")
	list_filter = ("viewed",)


@admin.register(Abuse_Report)
class Admin_Abuse_Report(admin.ModelAdmin):
	list_display = ("name", "email", "user", "complaint", "ip_address", "date_time", "viewed")
	list_filter = ("viewed",)
