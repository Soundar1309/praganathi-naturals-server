#!/usr/bin/env python3
"""
Quick setup script to create Django ecommerce application structure
"""

import os
import subprocess
import sys

def create_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)
    print(f"✅ Created directory: {path}")

def create_file(path, content):
    """Create file with content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ Created file: {path}")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Django Ecommerce Application...")
    
    # Create Django apps
    apps = ['users', 'products', 'carts', 'orders', 'notifications']
    
    for app in apps:
        create_directory(app)
        create_file(f"{app}/__init__.py", "")
        create_file(f"{app}/apps.py", f"""
from django.apps import AppConfig

class {app.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app}'
""")
        create_file(f"{app}/admin.py", f"""
from django.contrib import admin
# Register your models here.
""")
        create_file(f"{app}/models.py", f"""
from django.db import models
# Create your models here.
""")
        create_file(f"{app}/views.py", f"""
from django.shortcuts import render
# Create your views here.
""")
        create_file(f"{app}/urls.py", f"""
from django.urls import path
# Define your URL patterns here.
urlpatterns = [
]
""")
        create_file(f"{app}/serializers.py", f"""
from rest_framework import serializers
# Create your serializers here.
""")
    
    # Create ecommerce project files
    create_file("ecommerce/urls.py", '''
"""
URL configuration for ecommerce project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Health check endpoint
    path('up/', lambda request: HttpResponse('OK', status=200), name='health_check'),
    
    # API routes
    path('api/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('carts.urls')),
    path('api/', include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
''')
    
    create_file("ecommerce/wsgi.py", '''
"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()
''')
    
    create_file("ecommerce/asgi.py", '''
"""
ASGI config for ecommerce project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_asgi_application()
''')
    
    create_file("ecommerce/celery.py", '''
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

app = Celery('ecommerce')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
''')
    
    # Create .env file
    create_file(".env", '''# Django settings
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=ecommerce_development
DB_USER=sasikalavijayakumar
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Redis settings
REDIS_URL=redis://localhost:6379/0

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@ecommerce.com
''')
    
    # Create tasks.py
    create_file("tasks.py", '''
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_status_email(order_id, status):
    """Send email notification when order status changes"""
    try:
        from orders.models import Order
        order = Order.objects.select_related('user').get(id=order_id)
        subject = f'Order #{order.id} Status Update'
        message = f'Your order #{order.id} status has been updated to: {status}'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")

@shared_task
def cleanup_expired_carts():
    """Clean up carts that are older than 30 days"""
    from django.utils import timezone
    from datetime import timedelta
    from carts.models import Cart
    
    cutoff_date = timezone.now() - timedelta(days=30)
    expired_carts = Cart.objects.filter(updated_at__lt=cutoff_date)
    count = expired_carts.count()
    expired_carts.delete()
    
    return f'Cleaned up {count} expired carts'
''')
    
    print("\n📋 Next steps:")
    print("1. Install Python dependencies: pip install -r requirements.txt")
    print("2. Create PostgreSQL database: createdb ecommerce_development")
    print("3. Run migrations: python manage.py makemigrations && python manage.py migrate")
    print("4. Create superuser: python manage.py createsuperuser")
    print("5. Start server: python manage.py runserver")
    print("\n🔧 For complete setup, run: ./setup.sh")
    
    print("\n✅ Django application structure created successfully!")

if __name__ == "__main__":
    main() 