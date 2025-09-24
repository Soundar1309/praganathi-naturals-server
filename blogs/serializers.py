from rest_framework import serializers
from .models import Blog, BlogCategory, BlogTag, BlogComment
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug']

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description']

class BlogAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ['id', 'author_name', 'author_email', 'content', 'created_at', 'approved']
        read_only_fields = ['id', 'created_at', 'approved']

class BlogListSerializer(serializers.ModelSerializer):
    """Serializer for blog listing (shorter version)"""
    author = BlogAuthorSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    reading_time = serializers.ReadOnlyField()
    excerpt = serializers.ReadOnlyField()
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'summary', 'thumbnail', 'author', 
            'category', 'tags', 'published_date', 'created_at', 
            'reading_time', 'excerpt', 'featured'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'published_date']

class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog detail view (full version)"""
    author = BlogAuthorSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    reading_time = serializers.ReadOnlyField()
    comments = BlogCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'summary', 'content', 'thumbnail', 
            'hero_image', 'author', 'category', 'tags', 'status', 
            'featured', 'published_date', 'created_at', 'updated_at',
            'reading_time', 'meta_title', 'meta_description', 'comments'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'published_date']

class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating blogs (admin only)"""
    category_id = serializers.IntegerField(write_only=True, required=False)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Blog
        fields = [
            'title', 'summary', 'content', 'thumbnail', 'hero_image',
            'category_id', 'tag_ids', 'status', 'featured',
            'meta_title', 'meta_description'
        ]
    
    def validate_category_id(self, value):
        if value:
            try:
                BlogCategory.objects.get(id=value)
            except BlogCategory.DoesNotExist:
                raise serializers.ValidationError("Category does not exist.")
        return value
    
    def validate_tag_ids(self, value):
        if value:
            existing_tags = BlogTag.objects.filter(id__in=value)
            if len(existing_tags) != len(value):
                raise serializers.ValidationError("One or more tags do not exist.")
        return value
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Set author to current user
        validated_data['author'] = self.context['request'].user
        
        blog = Blog.objects.create(**validated_data)
        
        if category_id:
            blog.category_id = category_id
        
        if tag_ids:
            blog.tags.set(tag_ids)
        
        blog.save()
        return blog
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if category_id is not None:
            instance.category_id = category_id
        
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        
        instance.save()
        return instance
