#!/usr/bin/env python3
"""
Script to create sample data for Pragathi Natural Farms ecommerce API
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
    """Create sample categories and products for Pragathi Natural Farms"""
    
    print("🌱 Creating Sample Data for Pragathi Natural Farms")
    print("=" * 55)
    
    # Check if data already exists
    if Category.objects.exists():
        print("✅ Sample data already exists!")
        print(f"   Categories: {Category.objects.count()}")
        print(f"   Products: {Product.objects.count()}")
        return
    
    # Create farm-related categories
    categories_data = [
        {
            'name': 'Organic Vegetables',
            'description': 'Fresh organic vegetables grown without chemicals or pesticides'
        },
        {
            'name': 'Organic Fruits',
            'description': 'Natural fruits cultivated using sustainable farming practices'
        },
        {
            'name': 'Natural Grains & Pulses',
            'description': 'Organic grains, pulses, and cereals free from artificial additives'
        },
        {
            'name': 'Dairy Products',
            'description': 'Fresh dairy products from grass-fed animals'
        },
        {
            'name': 'Herbs & Spices',
            'description': 'Aromatic herbs and spices grown naturally'
        },
        {
            'name': 'Natural Honey & Oils',
            'description': 'Pure honey and cold-pressed oils from natural sources'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category.objects.create(**cat_data)
        categories.append(category)
        print(f"✅ Created category: {category.name}")
    
    # Create natural farm products
    products_data = [
        # Organic Vegetables
        {
            'title': 'Organic Tomatoes',
            'description': 'Fresh red tomatoes grown without pesticides, rich in vitamins and antioxidants',
            'price': 4.99,
            'stock': 150,
            'category': categories[0]  # Organic Vegetables
        },
        {
            'title': 'Organic Spinach',
            'description': 'Nutrient-rich green leafy spinach, perfect for healthy meals',
            'price': 3.49,
            'stock': 200,
            'category': categories[0]  # Organic Vegetables
        },
        {
            'title': 'Organic Carrots',
            'description': 'Sweet and crunchy orange carrots, naturally grown and vitamin-rich',
            'price': 2.99,
            'stock': 180,
            'category': categories[0]  # Organic Vegetables
        },
        {
            'title': 'Organic Broccoli',
            'description': 'Fresh green broccoli florets, packed with nutrients and fiber',
            'price': 5.49,
            'stock': 120,
            'category': categories[0]  # Organic Vegetables
        },
        
        # Organic Fruits
        {
            'title': 'Organic Apples',
            'description': 'Crisp and sweet apples grown in natural orchards without chemicals',
            'price': 6.99,
            'stock': 100,
            'category': categories[1]  # Organic Fruits
        },
        {
            'title': 'Organic Bananas',
            'description': 'Natural yellow bananas, perfect for smoothies and healthy snacking',
            'price': 3.99,
            'stock': 250,
            'category': categories[1]  # Organic Fruits
        },
        {
            'title': 'Organic Mangoes',
            'description': 'Sweet and juicy mangoes, naturally ripened and chemical-free',
            'price': 8.99,
            'stock': 80,
            'category': categories[1]  # Organic Fruits
        },
        {
            'title': 'Organic Strawberries',
            'description': 'Fresh red strawberries, naturally sweet and vitamin C rich',
            'price': 7.49,
            'stock': 90,
            'category': categories[1]  # Organic Fruits
        },
        
        # Natural Grains & Pulses
        {
            'title': 'Organic Brown Rice',
            'description': 'Whole grain brown rice, unpolished and nutrient-dense',
            'price': 12.99,
            'stock': 75,
            'category': categories[2]  # Natural Grains & Pulses
        },
        {
            'title': 'Organic Red Lentils',
            'description': 'Protein-rich red lentils, perfect for healthy dal and soups',
            'price': 8.49,
            'stock': 100,
            'category': categories[2]  # Natural Grains & Pulses
        },
        {
            'title': 'Organic Quinoa',
            'description': 'Super grain quinoa, complete protein source and gluten-free',
            'price': 15.99,
            'stock': 60,
            'category': categories[2]  # Natural Grains & Pulses
        },
        
        # Dairy Products
        {
            'title': 'Fresh Farm Milk',
            'description': 'Pure cow milk from grass-fed cows, no hormones or antibiotics',
            'price': 4.49,
            'stock': 200,
            'category': categories[3]  # Dairy Products
        },
        {
            'title': 'Organic Yogurt',
            'description': 'Creamy yogurt made from organic milk with live cultures',
            'price': 5.99,
            'stock': 150,
            'category': categories[3]  # Dairy Products
        },
        {
            'title': 'Farm Fresh Cheese',
            'description': 'Artisanal cheese made from farm-fresh milk using traditional methods',
            'price': 12.49,
            'stock': 80,
            'category': categories[3]  # Dairy Products
        },
        
        # Herbs & Spices
        {
            'title': 'Organic Turmeric Powder',
            'description': 'Pure turmeric powder with anti-inflammatory properties',
            'price': 6.99,
            'stock': 120,
            'category': categories[4]  # Herbs & Spices
        },
        {
            'title': 'Fresh Basil Leaves',
            'description': 'Aromatic basil leaves, perfect for cooking and teas',
            'price': 3.99,
            'stock': 100,
            'category': categories[4]  # Herbs & Spices
        },
        {
            'title': 'Organic Cumin Seeds',
            'description': 'Whole cumin seeds with intense flavor and digestive benefits',
            'price': 4.49,
            'stock': 90,
            'category': categories[4]  # Herbs & Spices
        },
        
        # Natural Honey & Oils
        {
            'title': 'Raw Wildflower Honey',
            'description': 'Unprocessed honey from wildflower nectar, rich in enzymes',
            'price': 18.99,
            'stock': 70,
            'category': categories[5]  # Natural Honey & Oils
        },
        {
            'title': 'Cold-Pressed Coconut Oil',
            'description': 'Virgin coconut oil extracted without heat, retains natural nutrients',
            'price': 14.99,
            'stock': 85,
            'category': categories[5]  # Natural Honey & Oils
        },
        {
            'title': 'Organic Sesame Oil',
            'description': 'Pure sesame oil with nutty flavor, perfect for cooking and massage',
            'price': 11.99,
            'stock': 95,
            'category': categories[5]  # Natural Honey & Oils
        }
    ]
    
    for prod_data in products_data:
        product = Product.objects.create(**prod_data)
        print(f"✅ Created product: {product.title} - ${product.price}")
    
    print("\n🎉 Pragathi Natural Farms sample data created successfully!")
    print(f"   Categories: {Category.objects.count()}")
    print(f"   Products: {Product.objects.count()}")
    print("\n🌱 You can now test the API endpoints:")
    print("   GET /api/products/categories/ - List all farm categories")
    print("   GET /api/products/products/ - List all natural products")
    print("   GET /api/products/products/?category_id=1 - Filter by category")
    print("\n🚀 Happy farming with Pragathi Natural Farms!")

if __name__ == "__main__":
    create_sample_data() 