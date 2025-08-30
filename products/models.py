from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Category model for product categorization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model equivalent to Rails Product model"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        default=10000.00,
        help_text="Original price of the product (default: 10000 Rs)"
    )
    offer_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Offer price of the product (automatically set to price)"
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        """Custom validation to ensure original_price >= offer_price"""
        super().clean()
        if self.offer_price and self.original_price < self.offer_price:
            raise ValidationError({
                'offer_price': 'Offer price cannot be greater than original price.'
            })
    
    def save(self, *args, **kwargs):
        """Ensure original_price is set to default if not provided and offer_price equals price"""
        if not self.original_price:
            self.original_price = 10000.00
        
        # Always set offer_price to the same value as price
        self.offer_price = self.price
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def available(self):
        return self.stock > 0
    
    @property
    def has_offer(self):
        """Check if product has an offer price"""
        return self.offer_price is not None and self.original_price > self.price
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if offer exists"""
        if self.has_offer:
            return round(((self.original_price - self.price) / self.original_price) * 100, 1)
        return 0 