"""
Payment models for Razorpay integration.
"""

from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()

class Payment(models.Model):
    """
    Model to store payment information from Razorpay.
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    razorpay_payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"Payment {self.razorpay_order_id} - {self.status}"
    
    @property
    def amount_in_paise(self):
        """Convert amount to paise for Razorpay."""
        return int(self.amount * 100)