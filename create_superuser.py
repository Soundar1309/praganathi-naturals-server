#!/usr/bin/env python3
"""
Script to create a Django superuser automatically
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import User

def create_superuser():
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser already exists!")
        return
    
    # Create superuser
    try:
        user = User.objects.create_superuser(
            email='admin@ecommerce.com',
            name='Admin User',
            password='admin123',
            role='admin'
        )
        print(f"✅ Superuser created successfully!")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.name}")
        print(f"   Password: admin123")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == "__main__":
    create_superuser() 