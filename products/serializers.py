from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'original_price', 'offer_price',
            'stock', 'image', 'category', 'category_id', 'created_at', 'updated_at',
            'has_offer', 'discount_percentage'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'has_offer', 'discount_percentage']
    
    def validate_category_id(self, value):
        try:
            Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")
        return value
    
    def validate(self, data):
        """Validate that original_price >= price"""
        original_price = data.get('original_price', 10000.00)
        price = data.get('price')
        
        if price and original_price and price >= original_price:
            raise serializers.ValidationError({
                'price': 'Price must be less than original price to show as an offer.'
            })
        
        return data
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        validated_data['category_id'] = category_id
        # offer_price will be automatically set to price in the model's save method
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            category_id = validated_data.pop('category_id')
            validated_data['category_id'] = category_id
        # offer_price will be automatically set to price in the model's save method
        return super().update(instance, validated_data) 