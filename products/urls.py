from django.urls import path
from . import views

urlpatterns = [
    # Category routes
    path('categories/', views.CategoryViewSet.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Product routes
    path('products/', views.ProductViewSet.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/with-variations/', views.ProductWithVariationsDetailView.as_view(), name='product_with_variations'),
    
    # Product variation routes
    path('variations/', views.ProductVariationViewSet.as_view(), name='variations'),
    path('variations/<int:pk>/', views.ProductVariationDetailView.as_view(), name='variation_detail'),
] 