from django.contrib import admin
from .models import Thread, Post


@admin.register(Thread)
class Admin_Thread(admin.ModelAdmin):
	def respond_to(sender, instance):
		return "Response Needed" if instance.unread and not instance.closed else ""
	ordering = ("closed", "-priority",)
	list_display = ("subject", "user", "datetime", "closed", "priority", "respond_to")

@admin.register(Post)
class Admin_Post(admin.ModelAdmin):
	list_display = ("thread", "user", "message", "datetime")