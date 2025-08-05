from django.urls import path
from . import views

urlpatterns = [
    # Cart routes
    path('carts/', views.CartView.as_view(), name='cart'),
    
    # CartItem routes
    path('cart_items/', views.CartItemViewSet.as_view(), name='cart_items'),
    path('cart_items/<int:pk>/', views.CartItemDetailView.as_view(), name='cart_item_detail'),
] 