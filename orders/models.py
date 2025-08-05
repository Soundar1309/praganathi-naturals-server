from django.db import models
from django.core.validators import MinValueValidator
from users.models import User, Address
from products.models import Product


class Order(models.Model):
    """Order model equivalent to Rails Order model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.status}"
    
    @property
    def is_paid(self):
        return self.status in ['paid', 'shipped', 'delivered']
    
    @property
    def is_cancelled(self):
        return self.status == 'cancelled'
    
    @property
    def is_delivered(self):
        return self.status == 'delivered'


class OrderItem(models.Model):
    """OrderItem model equivalent to Rails OrderItem model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.quantity}x {self.product.title} in Order #{self.order.id}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity 