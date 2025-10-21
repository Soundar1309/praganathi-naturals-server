from django.core.management.base import BaseCommand
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from orders.models import Order, OrderItem
from users.models import User


class Command(BaseCommand):
    help = 'Display comprehensive order statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed order information',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days to look back for recent orders (default: 30)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📊 ORDER STATISTICS'))
        self.stdout.write('=' * 60)

        # Basic counts
        total_orders = Order.objects.count()
        total_order_items = OrderItem.objects.count()
        total_users = User.objects.count()

        self.stdout.write(f'📦 Total Orders: {total_orders}')
        self.stdout.write(f'🛍️  Total Order Items: {total_order_items}')
        self.stdout.write(f'👥 Total Users: {total_users}')

        if total_orders == 0:
            self.stdout.write(self.style.WARNING('\n⚠️  No orders found in the database'))
            return

        # Revenue statistics
        revenue_stats = Order.objects.aggregate(
            total_revenue=Sum('total'),
            avg_order_value=Avg('total'),
            max_order_value=Sum('total')  # This will be the same as total for now
        )

        self.stdout.write(f'\n💰 REVENUE STATISTICS')
        self.stdout.write('-' * 30)
        self.stdout.write(f'Total Revenue: ₹{revenue_stats["total_revenue"] or 0:.2f}')
        self.stdout.write(f'Average Order Value: ₹{revenue_stats["avg_order_value"] or 0:.2f}')

        # Orders by status
        self.stdout.write(f'\n📈 ORDERS BY STATUS')
        self.stdout.write('-' * 30)
        for status, label in Order.STATUS_CHOICES:
            count = Order.objects.filter(status=status).count()
            percentage = (count / total_orders * 100) if total_orders > 0 else 0
            self.stdout.write(f'{label:12}: {count:4} ({percentage:5.1f}%)')

        # Time-based statistics
        now = timezone.now()
        days = options['days']
        start_date = now - timedelta(days=days)

        recent_orders = Order.objects.filter(created_at__gte=start_date).count()
        recent_revenue = Order.objects.filter(created_at__gte=start_date).aggregate(
            total=Sum('total')
        )['total'] or 0

        self.stdout.write(f'\n📅 LAST {days} DAYS')
        self.stdout.write('-' * 30)
        self.stdout.write(f'Orders: {recent_orders}')
        self.stdout.write(f'Revenue: ₹{recent_revenue:.2f}')

        # Monthly breakdown
        self.stdout.write(f'\n📊 MONTHLY BREAKDOWN')
        self.stdout.write('-' * 30)
        
        # Get orders from last 6 months
        for i in range(6):
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_start = month_start - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            
            month_orders = Order.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()
            
            month_revenue = Order.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).aggregate(total=Sum('total'))['total'] or 0
            
            month_name = month_start.strftime('%B %Y')
            self.stdout.write(f'{month_name:15}: {month_orders:3} orders, ₹{month_revenue:8.2f}')

        # Top customers
        self.stdout.write(f'\n👑 TOP CUSTOMERS')
        self.stdout.write('-' * 30)
        top_customers = User.objects.annotate(
            order_count=Count('orders'),
            total_spent=Sum('orders__total')
        ).filter(order_count__gt=0).order_by('-total_spent')[:5]

        for i, customer in enumerate(top_customers, 1):
            self.stdout.write(f'{i}. {customer.email:30} - {customer.order_count} orders, ₹{customer.total_spent or 0:.2f}')

        # Recent orders
        if options['detailed']:
            self.stdout.write(f'\n🕒 RECENT ORDERS')
            self.stdout.write('-' * 30)
            recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
            
            for order in recent_orders:
                status_emoji = {
                    'pending': '⏳',
                    'paid': '✅',
                    'shipped': '🚚',
                    'delivered': '📦',
                    'cancelled': '❌'
                }.get(order.status, '❓')
                
                self.stdout.write(
                    f'{status_emoji} Order #{order.id:4} - {order.user.email:25} - '
                    f'{order.status:10} - ₹{order.total:8.2f} - '
                    f'{order.created_at.strftime("%Y-%m-%d %H:%M")}'
                )

        self.stdout.write(f'\n✅ Statistics generated successfully!')
