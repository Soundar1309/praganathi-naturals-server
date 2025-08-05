from django.urls import path
from . import views

urlpatterns = [
    # Notification routes
    path('notifications/', views.NotificationViewSet.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_read_view, name='notification_mark_read'),
    path('notifications/mark_all_read/', views.mark_all_read_view, name='notifications_mark_all_read'),
    path('notifications/destroy_all/', views.destroy_all_view, name='notifications_destroy_all'),
    path('notifications/unread_count/', views.unread_count_view, name='notifications_unread_count'),
] 