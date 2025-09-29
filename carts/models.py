from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product, ProductVariation


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        unique_together = [
            ['cart', 'product'],
            ['cart', 'product_variation']
        ]
    
    def __str__(self):
        if self.product_variation:
            return f"{self.quantity}x {self.product_variation.display_name} of {self.product_variation.product.title} in {self.cart}"
        else:
            return f"{self.quantity}x {self.product.title} in {self.cart}"
    
    @property
    def subtotal(self):
        if self.product_variation:
            return self.product_variation.price * self.quantity
        else:
            return self.product.price * self.quantity
    
    @property
    def item_name(self):
        """Get the display name for the cart item"""
        if self.product_variation:
            return f"{self.product_variation.product.title} - {self.product_variation.display_name}"
        else:
            return self.product.title
    
    @property
    def item_price(self):
        """Get the price for the cart item"""
        if self.product_variation:
            return self.product_variation.price
        else:
            return self.product.price
    
    @property
    def item_image(self):
        """Get the image for the cart item"""
        if self.product_variation and self.product_variation.image:
            return self.product_variation.image
        elif self.product and self.product.image:
            return self.product.image
        return None
    
    def clean(self):
        """Ensure either product or product_variation is set, but not both"""
        from django.core.exceptions import ValidationError
        if not self.product and not self.product_variation:
            raise ValidationError('Either product or product_variation must be set.')
        if self.product and self.product_variation:
            raise ValidationError('Cannot set both product and product_variation.')
        if self.product_variation and self.product_variation.product != self.product:
            raise ValidationError('Product variation must belong to the specified product.') 