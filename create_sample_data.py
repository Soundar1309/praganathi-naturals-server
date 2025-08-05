#!/usr/bin/env python3
"""
Script to create sample data for testing the ecommerce API
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import User
from products.models import Category, Product

User = get_user_model()

def create_sample_data():
    """Create sample categories and products"""
    
    print("🎯 Creating Sample Data for Ecommerce API")
    print("=" * 50)
    
    # Check if data already exists
    if Category.objects.exists():
        print("✅ Sample data already exists!")
        print(f"   Categories: {Category.objects.count()}")
        print(f"   Products: {Product.objects.count()}")
        return
    
    # Create categories
    categories_data = [
        {
            'name': 'Electronics',
            'description': 'Electronic devices and gadgets'
        },
        {
            'name': 'Clothing',
            'description': 'Fashion and apparel'
        },
        {
            'name': 'Books',
            'description': 'Books and literature'
        },
        {
            'name': 'Home & Garden',
            'description': 'Home improvement and garden supplies'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category.objects.create(**cat_data)
        categories.append(category)
        print(f"✅ Created category: {category.name}")
    
    # Create products
    products_data = [
        {
            'title': 'iPhone 15 Pro',
            'description': 'Latest iPhone with advanced camera system and A17 Pro chip',
            'price': 999.99,
            'stock': 50,
            'category': categories[0]  # Electronics
        },
        {
            'title': 'Samsung Galaxy S24',
            'description': 'Premium Android smartphone with AI features',
            'price': 899.99,
            'stock': 30,
            'category': categories[0]  # Electronics
        },
        {
            'title': 'MacBook Air M3',
            'description': 'Lightweight laptop with M3 chip for productivity',
            'price': 1199.99,
            'stock': 25,
            'category': categories[0]  # Electronics
        },
        {
            'title': 'Nike Air Max 270',
            'description': 'Comfortable running shoes with Air Max technology',
            'price': 129.99,
            'stock': 100,
            'category': categories[1]  # Clothing
        },
        {
            'title': 'Levi\'s 501 Jeans',
            'description': 'Classic straight-fit jeans in blue denim',
            'price': 79.99,
            'stock': 75,
            'category': categories[1]  # Clothing
        },
        {
            'title': 'The Great Gatsby',
            'description': 'Classic American novel by F. Scott Fitzgerald',
            'price': 12.99,
            'stock': 200,
            'category': categories[2]  # Books
        },
        {
            'title': 'To Kill a Mockingbird',
            'description': 'Harper Lee\'s masterpiece about justice and racism',
            'price': 14.99,
            'stock': 150,
            'category': categories[2]  # Books
        },
        {
            'title': 'Garden Tool Set',
            'description': 'Complete set of essential garden tools',
            'price': 89.99,
            'stock': 40,
            'category': categories[3]  # Home & Garden
        },
        {
            'title': 'LED Desk Lamp',
            'description': 'Modern desk lamp with adjustable brightness',
            'price': 45.99,
            'stock': 60,
            'category': categories[3]  # Home & Garden
        }
    ]
    
    for prod_data in products_data:
        product = Product.objects.create(**prod_data)
        print(f"✅ Created product: {product.title} - ${product.price}")
    
    print("\n🎉 Sample data created successfully!")
    print(f"   Categories: {Category.objects.count()}")
    print(f"   Products: {Product.objects.count()}")
    print("\n📱 You can now test the API endpoints:")
    print("   GET /api/categories/ - List all categories")
    print("   GET /api/products/ - List all products")
    print("   GET /api/products/?category_id=1 - Filter by category")

if __name__ == "__main__":
    create_sample_data() 