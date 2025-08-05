from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'read', 'created_at']
    list_filter = ['read', 'created_at']
    search_fields = ['user__email', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at'] 