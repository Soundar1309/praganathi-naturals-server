from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import User


class Notification(models.Model):
    """Notification model equivalent to Rails Notification model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    
    # Generic foreign key for polymorphic association
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    notifiable = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.email}: {self.message[:50]}..."
    
    @classmethod
    def mark_all_read(cls, user):
        """Mark all notifications as read for a user"""
        return cls.objects.filter(user=user, read=False).update(read=True)
    
    @classmethod
    def unread_count(cls, user):
        """Get count of unread notifications for a user"""
        return cls.objects.filter(user=user, read=False).count() 