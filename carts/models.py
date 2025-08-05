from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product


class Cart(models.Model):
    """Cart model equivalent to Rails Cart model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carts'
    
    def __str__(self):
        return f"Cart for {self.user.email}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.cart_items.all())
    
    @property
    def item_count(self):
        return self.cart_items.count()


class CartItem(models.Model):
    """CartItem model equivalent to Rails CartItem model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.quantity}x {self.product.title} in {self.cart}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity 