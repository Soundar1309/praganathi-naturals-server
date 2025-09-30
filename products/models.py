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
    PRODUCT_TYPE_CHOICES = [
        ('solid', 'Solid (Rice, Pulses, etc.)'),
        ('liquid', 'Liquid (Oil, etc.)'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Original price of the product (automatically set to price if not provided)"
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
    unit = models.CharField(max_length=50, default='1 kg', help_text="Product unit (e.g., '1 kg', '500 ml', '10 nos')")
    product_type = models.CharField(
        max_length=10, 
        choices=PRODUCT_TYPE_CHOICES, 
        default='solid',
        help_text="Product type determines available quantity variants"
    )
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
        """Ensure original_price is set to price if not provided and offer_price equals price"""
        if not self.original_price:
            self.original_price = self.price
        
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
    
    def get_default_variation(self):
        """Get the default variation (250g for solid, 250ml for liquid)"""
        if self.product_type == 'solid':
            return self.variations.filter(quantity=250, unit='g').first()
        elif self.product_type == 'liquid':
            return self.variations.filter(quantity=250, unit='ml').first()
        else:
            # For other types, return the first variation or create a default one
            return self.variations.first()
    
    def get_available_variations(self):
        """Get all active variations ordered by quantity"""
        return self.variations.filter(is_active=True).order_by('quantity', 'unit')


class ProductVariation(models.Model):
    """Product variation model for different quantities and units"""
    UNIT_CHOICES = [
        ('ml', 'Milliliter'),
        ('l', 'Liter'),
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('nos', 'Numbers'),
        ('pcs', 'Pieces'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Original price of this variation"
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/variations/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_variations'
        unique_together = ['product', 'quantity', 'unit']
        ordering = ['quantity', 'unit']
    
    def __str__(self):
        return f"{self.product.title} - {self.quantity} {self.unit}"
    
    def clean(self):
        """Custom validation to ensure original_price >= price"""
        super().clean()
        if self.original_price and self.price and self.original_price < self.price:
            raise ValidationError({
                'original_price': 'Original price cannot be less than current price.'
            })
    
    def save(self, *args, **kwargs):
        """Ensure original_price is set to price if not provided"""
        if not self.original_price:
            self.original_price = self.price
        
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def available(self):
        return self.stock > 0
    
    @property
    def has_offer(self):
        """Check if variation has an offer price"""
        return self.original_price is not None and self.original_price > self.price
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if offer exists"""
        if self.has_offer:
            return round(((self.original_price - self.price) / self.original_price) * 100, 1)
        return 0
    
    @property
    def display_name(self):
        """Get display name for the variation"""
        return f"{self.quantity} {self.unit}" 