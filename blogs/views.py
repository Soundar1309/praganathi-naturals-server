from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Blog, BlogCategory, BlogTag, BlogComment
from .serializers import (
    BlogListSerializer, BlogDetailSerializer, BlogCreateUpdateSerializer,
    BlogCategorySerializer, BlogTagSerializer, BlogCommentSerializer
)

class BlogListView(generics.ListAPIView):
    """List all published blogs with filtering and search"""
    serializer_class = BlogListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Blog.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(content__icontains=search)
            )
        
        # Category filter
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Tag filter
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Featured filter
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)
        
        return queryset

class BlogDetailView(generics.RetrieveAPIView):
    """Get single blog detail"""
    serializer_class = BlogDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Blog.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags', 'comments')

class BlogCreateView(generics.CreateAPIView):
    """Create new blog (admin only)"""
    serializer_class = BlogCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save()

class BlogUpdateView(generics.UpdateAPIView):
    """Update blog (admin only)"""
    serializer_class = BlogCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Blog.objects.all()

class BlogDeleteView(generics.DestroyAPIView):
    """Delete blog (admin only)"""
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Blog.objects.all()

class BlogCategoryListView(generics.ListAPIView):
    """List all blog categories"""
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = BlogCategory.objects.all()

class BlogTagListView(generics.ListAPIView):
    """List all blog tags"""
    serializer_class = BlogTagSerializer
    permission_classes = [permissions.AllowAny]
    queryset = BlogTag.objects.all()

class BlogCommentCreateView(generics.CreateAPIView):
    """Create blog comment"""
    serializer_class = BlogCommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        blog_slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blog, slug=blog_slug, status='published')
        serializer.save(blog=blog)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def related_blogs(request, slug):
    """Get related blogs based on category and tags"""
    try:
        blog = Blog.objects.get(slug=slug, status='published')
        
        # Get blogs from same category
        category_blogs = Blog.objects.filter(
            category=blog.category,
            status='published'
        ).exclude(id=blog.id)[:3]
        
        # If not enough category blogs, get blogs with same tags
        if category_blogs.count() < 3:
            tag_blogs = Blog.objects.filter(
                tags__in=blog.tags.all(),
                status='published'
            ).exclude(id=blog.id).distinct()[:3]
            
            # Combine and deduplicate
            related = list(category_blogs) + list(tag_blogs)
            related = list(dict.fromkeys(related))[:3]  # Remove duplicates
        else:
            related = list(category_blogs)
        
        serializer = BlogListSerializer(related, many=True)
        return Response(serializer.data)
    
    except Blog.DoesNotExist:
        return Response(
            {'error': 'Blog not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_blogs(request):
    """Get featured blogs"""
    blogs = Blog.objects.filter(
        status='published',
        featured=True
    ).select_related('author', 'category').prefetch_related('tags')[:6]
    
    serializer = BlogListSerializer(blogs, many=True)
    return Response(serializer.data)