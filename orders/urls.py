from django.urls import path
from . import views

urlpatterns = [
    # Order routes
    path('orders/', views.OrderViewSet.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
] 