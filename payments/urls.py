"""
Payment URLs for Razorpay integration.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('details/<int:payment_id>/', views.get_payment_details, name='get_payment_details'),
    path('user-payments/', views.get_user_payments, name='get_user_payments'),
]
