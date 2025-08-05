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
        fields = ['id', 'title', 'description', 'price', 'stock', 'image', 'category', 'category_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_category_id(self, value):
        try:
            Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")
        return value
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        validated_data['category_id'] = category_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            category_id = validated_data.pop('category_id')
            validated_data['category_id'] = category_id
        return super().update(instance, validated_data) 