from django.urls import path
from . import views

urlpatterns = [
    # Order routes
    path('', views.OrderViewSet.as_view(), name='orders'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
] 