from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer, ProductVariationSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model"""
    product = ProductSerializer(read_only=True)
    product_variation = ProductVariationSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)
    product_variation_id = serializers.IntegerField(write_only=True, required=False)
    subtotal = serializers.ReadOnlyField()
    item_name = serializers.ReadOnlyField()
    item_price = serializers.ReadOnlyField()
    item_image = serializers.SerializerMethodField()
    effective_quantity = serializers.ReadOnlyField()
    effective_unit = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_variation', 'product_id', 'product_variation_id',
            'quantity', 'custom_quantity', 'custom_unit', 'subtotal', 'item_name', 
            'item_price', 'item_image', 'effective_quantity', 'effective_unit',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_item_image(self, obj):
        """Return the image URL for the cart item"""
        if obj.product_variation:
            # For variations, check variation image first, then parent product image
            if obj.product_variation.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.product_variation.image.url)
                return obj.product_variation.image.url
            elif obj.product_variation.product and obj.product_variation.product.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.product_variation.product.image.url)
                return obj.product_variation.product.image.url
        elif obj.product and obj.product.image:
            # For regular products, use product image
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None
    
    
    def validate_product_id(self, value):
        from products.models import Product
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value
    
    def validate_product_variation_id(self, value):
        from products.models import ProductVariation
        try:
            ProductVariation.objects.get(id=value)
        except ProductVariation.DoesNotExist:
            raise serializers.ValidationError("Product variation does not exist.")
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
    
    def validate_custom_quantity(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Custom quantity must be greater than 0.")
        return value
    
    def validate(self, data):
        """Validate that either product_id or product_variation_id is provided, but not both"""
        product_id = data.get('product_id')
        product_variation_id = data.get('product_variation_id')
        
        if not product_id and not product_variation_id:
            raise serializers.ValidationError("Either product_id or product_variation_id must be provided.")
        
        if product_id and product_variation_id:
            raise serializers.ValidationError("Cannot provide both product_id and product_variation_id.")
        
        # Validate custom quantity and unit
        custom_quantity = data.get('custom_quantity')
        custom_unit = data.get('custom_unit')
        
        if custom_quantity and not custom_unit:
            raise serializers.ValidationError("Custom unit must be provided when custom quantity is set.")
        if custom_unit and not custom_quantity:
            raise serializers.ValidationError("Custom quantity must be provided when custom unit is set.")
        
        return data
    
    def create(self, validated_data):
        request = self.context['request']
        
        # Get or create cart for the user (authenticated or anonymous)
        cart = Cart.get_or_create_cart(request)
        
        # Handle product variation
        if 'product_variation_id' in validated_data:
            product_variation_id = validated_data.pop('product_variation_id')
            
            # Check if cart item already exists for this variation
            try:
                cart_item = CartItem.objects.get(cart=cart, product_variation_id=product_variation_id)
                cart_item.quantity += validated_data.get('quantity', 1)
                cart_item.save()
                return cart_item
            except CartItem.DoesNotExist:
                validated_data['cart'] = cart
                validated_data['product_variation_id'] = product_variation_id
                return super().create(validated_data)
        
        # Handle regular product
        elif 'product_id' in validated_data:
            product_id = validated_data.pop('product_id')
            
            # Check if cart item already exists for this product
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