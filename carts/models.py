from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product


class Cart(models.Model):
    """Cart model equivalent to Rails Cart model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carts'
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        else:
            return f"Anonymous cart {self.session_key}"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.cart_items.all())
    
    @property
    def item_count(self):
        return self.cart_items.count()
    
    @classmethod
    def get_or_create_cart(cls, request):
        """Get or create cart for authenticated or anonymous user"""
        if request.user.is_authenticated:
            cart, created = cls.objects.get_or_create(user=request.user)
        else:
            # Ensure session exists and is saved
            if not request.session.session_key:
                request.session.create()
                request.session.save()
            
            session_key = request.session.session_key
            cart, created = cls.objects.get_or_create(session_key=session_key, user=None)
        return cart


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