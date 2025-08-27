from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('delivery', 'Delivery'),
    ]
    
    # Override username field to be nullable and not required
    username = models.CharField(max_length=150, null=True, blank=True, unique=True)
    first_name = None
    last_name = None
    
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)  # Make name required
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ])
    wishlist = models.JSONField(default=list, blank=True)  # Array of product IDs
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Changed from username to name
    
    objects = CustomUserManager()
    
    def clean(self):
        super().clean()
        # Ensure username is not required
        if not self.username:
            self.username = None
    
    def save(self, *args, **kwargs):
        # Ensure username is not required
        if not self.username:
            self.username = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other addresses for this user to not default
            Address.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}"
