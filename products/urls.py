from django.urls import path
from . import views

urlpatterns = [
    # Category routes
    path('categories/', views.CategoryViewSet.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Product routes
    path('products/', views.ProductViewSet.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
] 