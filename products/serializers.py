from rest_framework import serializers
from .models import Category, Product, ProductVariation


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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'original_price', 'offer_price',
            'stock', 'unit', 'image', 'image_url', 'category', 'category_id', 'created_at', 'updated_at',
            'has_offer', 'discount_percentage'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'has_offer', 'discount_percentage']
    
    def get_image_url(self, obj):
        """Return the image URL if image exists"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def validate_category_id(self, value):
        try:
            Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")
        return value
    
    def validate(self, data):
        """Validate that original_price >= price"""
        original_price = data.get('original_price')
        price = data.get('price')
        
        # If original_price is not provided, it will be set to price in the model's save method
        if original_price and price and price >= original_price:
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


class ProductVariationSerializer(serializers.ModelSerializer):
    """Serializer for ProductVariation model"""
    product_title = serializers.CharField(source='product.title', read_only=True)
    display_name = serializers.CharField(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariation
        fields = [
            'id', 'product', 'product_title', 'quantity', 'unit', 'price', 
            'original_price', 'stock', 'image', 'image_url', 'is_active', 'created_at', 
            'updated_at', 'available', 'has_offer', 'discount_percentage', 'display_name'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'available', 'has_offer', 
            'discount_percentage', 'display_name', 'product_title'
        ]
    
    def get_image_url(self, obj):
        """Return the image URL if image exists"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def validate(self, data):
        """Validate that original_price >= price"""
        original_price = data.get('original_price')
        price = data.get('price')
        
        if original_price and price and price >= original_price:
            raise serializers.ValidationError({
                'price': 'Price must be less than original price to show as an offer.'
            })
        
        return data


class ProductWithVariationsSerializer(serializers.ModelSerializer):
    """Serializer for Product model with variations"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'original_price', 'offer_price',
            'stock', 'unit', 'image', 'image_url', 'category', 'category_id', 'created_at', 'updated_at',
            'has_offer', 'discount_percentage', 'variations'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'has_offer', 'discount_percentage']
    
    def get_image_url(self, obj):
        """Return the image URL if image exists"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def validate_category_id(self, value):
        try:
            Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")
        return value
    
    def validate(self, data):
        """Validate that original_price >= price"""
        original_price = data.get('original_price')
        price = data.get('price')
        
        # If original_price is not provided, it will be set to price in the model's save method
        if original_price and price and price >= original_price:
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