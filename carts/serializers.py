from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model"""
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_product_id(self, value):
        from products.models import Product
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    
    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user = self.context['request'].user
        
        # Get or create cart for the user
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Check if cart item already exists
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.quantity += validated_data.get('quantity', 1)
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            validated_data['cart'] = cart
            validated_data['product_id'] = product_id
            return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model"""
    cart_items = CartItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total', 'item_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at'] 