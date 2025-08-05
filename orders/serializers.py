from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import UserSerializer, AddressSerializer
from products.serializers import ProductSerializer
from users.models import User


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    product = ProductSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal', 'created_at']
        read_only_fields = ['id', 'price', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    order_items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    delivery = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'address', 'delivery', 'status', 'total', 
            'order_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    address_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = ['address_id']
    
    def validate_address_id(self, value):
        user = self.context['request'].user
        try:
            user.addresses.get(id=value)
        except user.addresses.model.DoesNotExist:
            raise serializers.ValidationError("Invalid address for this user.")
        return value


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating orders"""
    delivery_id = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = Order
        fields = ['status', 'delivery_id']
    
    def validate(self, attrs):
        user = self.context['request'].user
        order = self.instance
        
        # Status transition validation
        allowed_transitions = {
            'pending': ['paid', 'cancelled'],
            'paid': ['shipped', 'cancelled'],
            'shipped': ['delivered', 'cancelled'],
            'delivered': [],
            'cancelled': []
        }
        
        new_status = attrs.get('status')
        if new_status:
            if user.role == 'admin':
                if new_status not in allowed_transitions.get(order.status, []):
                    raise serializers.ValidationError("Invalid status transition.")
            elif user.role == 'delivery' and order.delivery == user:
                if order.status == 'shipped' and new_status == 'delivered':
                    pass  # Valid transition
                else:
                    raise serializers.ValidationError("Unauthorized or invalid transition.")
            else:
                raise serializers.ValidationError("Unauthorized to change order status.")
        
        # Delivery assignment validation
        delivery_id = attrs.get('delivery_id')
        if delivery_id and user.role == 'admin':
            try:
                delivery_user = User.objects.get(id=delivery_id, role='delivery')
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid delivery user.")
        
        return attrs 