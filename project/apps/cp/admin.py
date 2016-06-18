from django.contrib import admin
from .models import Notification
from .models import Announcement

# Register your models here.
@admin.register(Notification)
class Admin_Notification(admin.ModelAdmin):
	list_display = ("user", "message", "datetime", "unread")
	readonly_fields = ("url",)


@admin.register(Announcement)
class Admin_Notification(admin.ModelAdmin):
	list_display = ("subject", "message", "datetime", "broadcast")