"""
Payment serializers for Razorpay integration.
"""

from rest_framework import serializers
from .models import Payment

class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating Razorpay orders."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)
    currency = serializers.CharField(max_length=3, default='INR')
    order_id = serializers.IntegerField(required=False, help_text="Order ID to associate with payment")

class VerifyPaymentSerializer(serializers.Serializer):
    """Serializer for verifying Razorpay payments."""
    razorpay_order_id = serializers.CharField(max_length=255)
    razorpay_payment_id = serializers.CharField(max_length=255)
    razorpay_signature = serializers.CharField(max_length=255)

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'razorpay_order_id',
            'razorpay_payment_id',
            'amount',
            'currency',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
