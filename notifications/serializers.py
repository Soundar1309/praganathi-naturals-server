from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    class Meta:
        model = Notification
        fields = ['id', 'message', 'read', 'notifiable', 'created_at', 'updated_at']
        read_only_fields = ['id', 'message', 'notifiable', 'created_at', 'updated_at'] 