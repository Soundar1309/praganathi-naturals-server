from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from django.shortcuts import get_object_or_404
from users.models import User
from carts.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer
from notifications.models import Notification


class OrderViewSet(generics.ListCreateAPIView):
    """Order views equivalent to Rails OrdersController"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.select_related('address', 'delivery', 'user').prefetch_related('order_items__product').all()
        elif user.role == 'delivery':
            return Order.objects.filter(delivery=user).select_related('address', 'delivery', 'user').prefetch_related('order_items__product')
        else:
            return user.orders.select_related('address', 'delivery').prefetch_related('order_items__product')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Get or create cart for the user
            try:
                cart = user.cart
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=user)
            
            # Check if cart exists and has items
            if not cart or not cart.cart_items.exists():
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
            
            address_id = serializer.validated_data['address_id']
            address = user.addresses.get(id=address_id)
            
            # Create order
            order = Order.objects.create(
                user=user,
                address=address,
                status='pending',
                total=0
            )
            
            order_total = 0
            
            # Process cart items
            for cart_item in cart.cart_items.select_related('product', 'product_variation__product').all():
                # Determine which product to use
                if cart_item.product:
                    product = cart_item.product
                    price = product.price
                elif cart_item.product_variation:
                    product = cart_item.product_variation.product
                    price = cart_item.product_variation.price
                else:
                    continue  # Skip items without product or variation
                
                # Check stock availability
                if product.stock < cart_item.quantity:
                    raise serializers.ValidationError(f"Insufficient stock for {product.title}")
                
                # Create order item
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart_item.quantity,
                    price=price
                )
                
                # Update product stock
                product.stock -= cart_item.quantity
                product.save()
                
                order_total += price * cart_item.quantity
            
            # Update order total
            order.total = order_total
            order.save()
            
            # Clear cart
            cart.cart_items.all().delete()
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    """Order detail view"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.select_related('address', 'delivery', 'user').prefetch_related('order_items__product').all()
        elif user.role == 'delivery':
            return Order.objects.filter(delivery=user).select_related('address', 'delivery', 'user').prefetch_related('order_items__product')
        else:
            return user.orders.select_related('address', 'delivery').prefetch_related('order_items__product')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderSerializer
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        serializer = self.get_serializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            status_changed = False
            delivery_assigned = False
            
            # Handle delivery assignment
            delivery_id = serializer.validated_data.get('delivery_id')
            if delivery_id and user.role == 'admin':
                delivery_user = User.objects.get(id=delivery_id, role='delivery')
                order.delivery = delivery_user
                delivery_assigned = True
                
                # Create notification for delivery user
                Notification.objects.create(
                    user=delivery_user,
                    notifiable=order,
                    message=f"You have been assigned to deliver order #{order.id}",
                    read=False
                )
            
            # Handle status changes
            new_status = serializer.validated_data.get('status')
            if new_status:
                order.status = new_status
                status_changed = True
                
                # Create notification for user
                Notification.objects.create(
                    user=order.user,
                    notifiable=order,
                    message=f"Your order status changed to {new_status}",
                    read=False
                )
            
            order.save()
            
            # Send email notifications (placeholder for email functionality)
            if status_changed:
                # OrderMailer.status_changed(order).deliver_later equivalent
                pass
            
            if delivery_assigned:
                # OrderMailer.delivery_assigned(order).deliver_later equivalent
                pass
            
            return Response(OrderSerializer(order).data)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 