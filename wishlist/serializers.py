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
        user = self.context['request'].user
        product_id = validated_data.pop('product_id')
        
        # Check if item already exists
        if WishlistItem.objects.filter(user=user, product_id=product_id).exists():
            raise serializers.ValidationError("Product is already in your wishlist")
        
        # Create wishlist item
        wishlist_item = WishlistItem.objects.create(
            user=user,
            product_id=product_id
        )
        
        # Update user's wishlist field
        user.wishlist.append(product_id)
        user.save()
        
        return wishlist_item
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product_id'] = instance.product.id
        return representation
