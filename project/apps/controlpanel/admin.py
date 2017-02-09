from django.contrib import admin
from .models import Broadcast, Notification



@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
	"""
	Admin for Party model.
	"""
	show_full_result_count = False
	list_display = ("content", "icon", "url", "is_staff", "datetime")
	raw_id_fields = ("readers",)



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	"""
	Admin for Party model.
	"""
	show_full_result_count = False
	list_display = ("recipient", "unread", "content", "icon", "url", "datetime")
	raw_id_fields = ("recipient",)


	def get_queryset(self, request):
		"""
		Chain prefetch_related onto queryset to make it more efficient.
		"""
		return (
			super(__class__, self)
				.get_queryset(request)
				.prefetch_related("recipient")
			)