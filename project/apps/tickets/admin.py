from django.contrib import admin
from .models import Thread, Post



@admin.register(Thread)
class Admin_Thread(admin.ModelAdmin):
	list_display = ("subject", "user", "type", "priority", "date_time", "closed")



@admin.register(Post)
class Admin_Post(admin.ModelAdmin):
	list_display = ("thread", "user", "date_time")