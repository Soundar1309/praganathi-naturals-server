#!/usr/bin/env python3
"""
Script to populate the database with new categories and products
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Category, Product

def clear_existing_data():
    """Clear all existing categories and products"""
    print("🗑️  Clearing existing data...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    print("✅ Existing data cleared")

def create_categories():
    """Create the new categories based on the provided list"""
    print("📂 Creating categories...")
    
    categories_data = [
        {"name": "Agarbathi", "description": "Traditional incense sticks and spiritual products"},
        {"name": "Annapodi", "description": "Rice flour and related products"},
        {"name": "Dhoop sticks", "description": "Aromatic dhoop sticks for spiritual purposes"},
        {"name": "Dry Graphs", "description": "Dried fruits and snacks"},
        {"name": "Dry Nuts", "description": "Assorted dry nuts and seeds"},
        {"name": "Flakes", "description": "Various types of flakes and cereals"},
        {"name": "Honey", "description": "Pure honey and honey products"},
        {"name": "Maavu", "description": "Traditional flour mixes"},
        {"name": "Malt", "description": "Malt-based health drinks and powders"},
        {"name": "Masala", "description": "Spice mixes and seasonings"},
        {"name": "Millet", "description": "Various types of millets"},
        {"name": "Noodles", "description": "Different varieties of noodles"},
        {"name": "Nuts and Seeds", "description": "Mixed nuts and seeds"},
        {"name": "Oil", "description": "Cooking oils and essential oils"},
        {"name": "Paruppu", "description": "Lentils and pulses"},
        {"name": "Payiru", "description": "Green gram and related products"},
        {"name": "Rasapodi", "description": "Rasam powder and related products"},
        {"name": "Rice", "description": "Various types of rice"},
        {"name": "Rock Salt", "description": "Natural rock salt and salt products"},
        {"name": "Soap", "description": "Natural soaps and cleaning products"},
        {"name": "Soup", "description": "Soup powders and mixes"},
        {"name": "Spices", "description": "Whole spices and ground spices"},
        {"name": "Tea", "description": "Tea leaves and tea products"},
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category.objects.create(**cat_data)
        categories.append(category)
        print(f"✅ Created category: {category.name}")
    
    print(f"🎉 Created {len(categories)} categories")
    return categories

def create_single_products():
    """Create the single products that don't belong to specific categories"""
    print("📦 Creating single products...")
    
    single_products = [
        {"title": "Digestive Bites", "description": "Natural digestive health supplement", "price": 299.99, "stock": 50},
        {"title": "Dish Wash Powder", "description": "Eco-friendly dish washing powder", "price": 89.99, "stock": 100},
        {"title": "Femi9 Pad", "description": "Natural feminine hygiene product", "price": 199.99, "stock": 75},
        {"title": "Floor Cleaner", "description": "Natural floor cleaning solution", "price": 149.99, "stock": 60},
        {"title": "Ghee", "description": "Pure clarified butter", "price": 399.99, "stock": 40},
        {"title": "Health Mix", "description": "Nutritious health drink mix", "price": 249.99, "stock": 80},
        {"title": "Karuppu Kavuni Kanji Powder", "description": "Traditional black rice porridge powder", "price": 179.99, "stock": 45},
        {"title": "Karuppu Kollu", "description": "Black horse gram", "price": 129.99, "stock": 70},
        {"title": "Karuppu Sundal", "description": "Black chickpea snack", "price": 159.99, "stock": 55},
        {"title": "Karuppu Ulundu Kanji Powder", "description": "Black urad dal porridge powder", "price": 189.99, "stock": 50},
        {"title": "Kunkumam", "description": "Traditional vermilion powder", "price": 79.99, "stock": 90},
        {"title": "Manjal", "description": "Natural turmeric powder", "price": 99.99, "stock": 85},
        {"title": "Mosquito Coil", "description": "Natural mosquito repellent coil", "price": 69.99, "stock": 120},
    ]
    
    products = []
    for prod_data in single_products:
        product = Product.objects.create(**prod_data)
        products.append(product)
        print(f"✅ Created product: {product.title} - ₹{product.price}")
    
    print(f"🎉 Created {len(products)} single products")
    return products

def create_category_products():
    """Create products for each category based on the subcategory counts"""
    print("🏷️  Creating category products...")
    
    # Category to subcategory mapping
    category_subcategories = {
        "Agarbathi": 2,
        "Annapodi": 5,
        "Dhoop sticks": 4,
        "Dry Graphs": 2,
        "Dry Nuts": 3,
        "Flakes": 8,
        "Honey": 4,
        "Maavu": 4,
        "Malt": 3,
        "Masala": 8,
        "Millet": 7,
        "Noodles": 5,
        "Nuts and Seeds": 2,
        "Oil": 4,
        "Paruppu": 10,
        "Payiru": 2,
        "Rasapodi": 5,
        "Rice": 7,
        "Rock Salt": 3,
        "Soap": 8,
        "Soup": 4,
        "Spices": 14,
        "Tea": 4,
    }
    
    total_products = 0
    
    for category_name, subcategory_count in category_subcategories.items():
        try:
            category = Category.objects.get(name=category_name)
            
            # Create products for this category
            for i in range(1, subcategory_count + 1):
                product_name = f"{category_name} Product {i}"
                product = Product.objects.create(
                    title=product_name,
                    description=f"High-quality {category_name.lower()} product",
                    price=round(100 + (i * 50) + (hash(category_name) % 200), 2),
                    stock=50 + (i * 10),
                    category=category
                )
                total_products += 1
                print(f"✅ Created: {product.title} (₹{product.price}) - {category.name}")
                
        except Category.DoesNotExist:
            print(f"❌ Category not found: {category_name}")
    
    print(f"🎉 Created {total_products} category products")
    return total_products

def main():
    """Main function to populate the database"""
    print("🚀 Starting database population...")
    print("=" * 50)
    
    # Clear existing data
    clear_existing_data()
    
    # Create categories
    categories = create_categories()
    
    # Create single products (no category)
    single_products = create_single_products()
    
    # Create category products
    category_products = create_category_products()
    
    # Summary
    print("=" * 50)
    print("📊 POPULATION SUMMARY:")
    print(f"   Categories: {Category.objects.count()}")
    print(f"   Single Products: {len(single_products)}")
    print(f"   Category Products: {category_products}")
    print(f"   Total Products: {Product.objects.count()}")
    print(f"   Total Items: {Category.objects.count() + Product.objects.count()}")
    print("=" * 50)
    print("🎉 Database population completed successfully!")

if __name__ == "__main__":
    main() 