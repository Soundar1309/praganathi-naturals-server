from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import Category, Product, ProductVariation
from .serializers import CategorySerializer, ProductSerializer, ProductVariationSerializer, ProductWithVariationsSerializer
from .permissions import IsAdminUser


class CategoryViewSet(generics.ListCreateAPIView):
    """Category views equivalent to Rails CategoriesController"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Category detail view"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]


class ProductViewSet(generics.ListCreateAPIView):
    """Product views equivalent to Rails ProductsController"""
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category_id']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()
        
        # Filter by category_id
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Search functionality equivalent to Rails ILIKE
        search_query = self.request.query_params.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Product detail view"""
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]


class ProductWithVariationsDetailView(generics.RetrieveAPIView):
    """Product detail view with variations"""
    queryset = Product.objects.select_related('category').prefetch_related('variations').all()
    serializer_class = ProductWithVariationsSerializer
    permission_classes = [permissions.AllowAny]


class ProductVariationViewSet(generics.ListCreateAPIView):
    """Product variation views"""
    serializer_class = ProductVariationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'unit', 'is_active']
    ordering_fields = ['quantity', 'price', 'created_at']
    ordering = ['quantity', 'unit']
    
    def get_queryset(self):
        queryset = ProductVariation.objects.select_related('product').all()
        
        # Filter by product_id
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        return queryset
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]


class ProductVariationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Product variation detail view"""
    queryset = ProductVariation.objects.select_related('product').all()
    serializer_class = ProductVariationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [permissions.AllowAny()] 