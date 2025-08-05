from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(generics.ListAPIView):
    """Notification views equivalent to Rails NotificationsController"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def mark_read_view(request, pk):
    """Mark notification as read equivalent to Rails NotificationsController#mark_read"""
    try:
        notification = Notification.objects.get(id=pk, user=request.user)
        notification.read = True
        notification.save()
        return Response(NotificationSerializer(notification).data)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_read_view(request):
    """Mark all notifications as read equivalent to Rails NotificationsController#mark_all_read"""
    count = Notification.mark_all_read(request.user)
    return Response({'message': f'{count} notifications marked as read'})


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def destroy_all_view(request):
    """Delete all notifications equivalent to Rails NotificationsController#destroy_all"""
    count = Notification.objects.filter(user=request.user).delete()[0]
    return Response({'message': f'{count} notifications deleted'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_count_view(request):
    """Get unread count equivalent to Rails NotificationsController#unread_count"""
    count = Notification.unread_count(request.user)
    return Response({'unread_count': count}) 