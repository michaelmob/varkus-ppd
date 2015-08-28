from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Thread, Post


@admin.register(Thread)
class Admin_Thread(admin.ModelAdmin):
	def view_on_site(self, obj):
		return reverse("tickets-thread", args=(obj.id,))
	
	list_display = ("subject", "user", "type", "priority", "date_time", "closed")
	list_filter = ("closed", "priority")


@admin.register(Post)
class Admin_Post(admin.ModelAdmin):
	list_display = ("thread", "user", "date_time")
