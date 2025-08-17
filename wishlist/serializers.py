from rest_framework import serializers
from .models import WishlistItem
from products.serializers import ProductSerializer

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'product_id', 'added_at']
        read_only_fields = ['id', 'added_at']
    
    def create(self, validated_data):
        request = self.context['request']
        product_id = validated_data.pop('product_id')
        
        # Check if item already exists
        if WishlistItem.check_wishlist_status(request, product_id):
            raise serializers.ValidationError("Product is already in your wishlist")
        
        # Get or create wishlist item using the new method
        from products.models import Product
        product = Product.objects.get(id=product_id)
        wishlist_item = WishlistItem.get_or_create_wishlist_item(request, product)
        
        # Update user's wishlist field if authenticated
        if request.user.is_authenticated and product_id not in request.user.wishlist:
            request.user.wishlist.append(product_id)
            request.user.save()
        
        return wishlist_item
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product_id'] = instance.product.id
        return representation
