from django.contrib import admin
from .models import Thread, Post



@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
	"""
	Admin for Thread model.
	"""
	show_full_result_count = False
	ordering = ("closed", "-priority",)
	list_display = (
		"subject", "user", "datetime", "closed", "priority", "response"
	)
	raw_id_fields = ("user", "last_user")


	def response(sender, instance):
		"""
		Custom column to show whether or not the ticket needs attention.
		"""
		response_needed = instance.unread and not instance.closed
		return "Response Needed" if response_needed else ""



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	"""
	Admin for Post model.
	"""
	show_full_result_count = False
	list_display = ("thread", "user", "message", "datetime")
	raw_id_fields = ("thread", "user")