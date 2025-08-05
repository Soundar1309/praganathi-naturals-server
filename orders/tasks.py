from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from orders.models import Order


@shared_task
def send_order_status_email(order_id, status):
    """Send email notification when order status changes"""
    try:
        order = Order.objects.select_related('user').get(id=order_id)
        subject = f'Order #{order.id} Status Update'
        message = f'Your order #{order.id} status has been updated to: {status}'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        pass


@shared_task
def send_delivery_assignment_email(order_id):
    """Send email notification when delivery is assigned"""
    try:
        order = Order.objects.select_related('user', 'delivery').get(id=order_id)
        subject = f'Delivery Assignment - Order #{order.id}'
        message = f'You have been assigned to deliver order #{order.id}'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.delivery.email],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        pass


@shared_task
def cleanup_expired_carts():
    """Clean up carts that are older than 30 days"""
    from django.utils import timezone
    from datetime import timedelta
    from carts.models import Cart
    
    cutoff_date = timezone.now() - timedelta(days=30)
    expired_carts = Cart.objects.filter(updated_at__lt=cutoff_date)
    count = expired_carts.count()
    expired_carts.delete()
    
    return f'Cleaned up {count} expired carts' 