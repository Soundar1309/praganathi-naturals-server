from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from orders.models import Order, OrderItem
from products.models import Product, Category
from payments.models import Payment


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Admin dashboard statistics endpoint.
    Returns comprehensive statistics for the admin dashboard.
    """
    # Check if user is admin
    if request.user.role != 'admin':
        return Response(
            {'error': 'Access denied. Admin role required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Get current date and calculate date ranges
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)
        
        # Basic metrics
        total_orders = Order.objects.count()
        total_users = User.objects.count()
        
        # Total products sold (sum of all order item quantities)
        total_products_sold = OrderItem.objects.aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        # Total revenue (sum of all completed payments)
        total_revenue = Payment.objects.filter(
            status='completed'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Orders per day (last 30 days)
        orders_per_day = Order.objects.filter(
            created_at__gte=thirty_days_ago
        ).annotate(
            date=TruncDay('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Format dates for frontend
        orders_per_day_formatted = []
        for item in orders_per_day:
            orders_per_day_formatted.append({
                'date': item['date'].strftime('%Y-%m-%d'),
                'count': item['count']
            })
        
        # Sales by category (last 30 days)
        sales_by_category = OrderItem.objects.filter(
            order__created_at__gte=thirty_days_ago,
            order__status__in=['paid', 'shipped', 'delivered']
        ).values(
            'product__category__name'
        ).annotate(
            value=Sum('price')
        ).order_by('-value')
        
        # Format category data
        sales_by_category_formatted = []
        for item in sales_by_category:
            category_name = item['product__category__name'] or 'Uncategorized'
            sales_by_category_formatted.append({
                'category': category_name,
                'value': float(item['value'])
            })
        
        # Monthly revenue trends (last 12 months)
        monthly_revenue = Payment.objects.filter(
            status='completed',
            created_at__gte=now - timedelta(days=365)
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            value=Sum('amount')
        ).order_by('month')
        
        # Format monthly revenue data
        monthly_revenue_formatted = []
        month_names = {
            '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
            '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
            '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
        }
        
        for item in monthly_revenue:
            month_date = item['month']
            year_month = month_date.strftime('%Y-%m')
            year, month = year_month.split('-')
            month_name = month_names.get(month, month)
            monthly_revenue_formatted.append({
                'month': f"{month_name} {year}",
                'value': float(item['value'])
            })
        
        # Recent orders (last 10)
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
        recent_orders_data = []
        for order in recent_orders:
            recent_orders_data.append({
                'id': order.id,
                'user_email': order.user.email,
                'status': order.status,
                'total': float(order.total),
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        # Top selling products (last 30 days)
        top_products = OrderItem.objects.filter(
            order__created_at__gte=thirty_days_ago,
            order__status__in=['paid', 'shipped', 'delivered']
        ).values(
            'product__title'
        ).annotate(
            quantity_sold=Sum('quantity'),
            revenue=Sum('price')
        ).order_by('-quantity_sold')[:10]
        
        top_products_data = []
        for product in top_products:
            top_products_data.append({
                'title': product['product__title'],
                'quantity_sold': product['quantity_sold'],
                'revenue': float(product['revenue'])
            })
        
        return Response({
            'total_orders': total_orders,
            'total_products_sold': total_products_sold,
            'total_users': total_users,
            'total_revenue': float(total_revenue),
            'orders_per_day': orders_per_day_formatted,
            'sales_by_category': sales_by_category_formatted,
            'monthly_revenue': monthly_revenue_formatted,
            'recent_orders': recent_orders_data,
            'top_products': top_products_data,
            'last_updated': now.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error fetching dashboard data: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
