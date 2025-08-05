#!/usr/bin/env python3
"""
Script to add suitable images for each product based on their categories and names
"""

import os
import sys
import django
import requests
from urllib.parse import urlparse
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Category, Product

def download_image(url, filename):
    """Download image from URL and save to local path"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Create products directory if it doesn't exist
        products_dir = Path('media/products')
        products_dir.mkdir(parents=True, exist_ok=True)
        
        # Save image
        file_path = products_dir / filename
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        return f'products/{filename}'
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return None

def get_image_urls():
    """Return a mapping of product types to suitable image URLs"""
    return {
        # Agarbathi (Incense)
        'agarbathi': [
            'https://images.unsplash.com/photo-1602928321679-711a8c0c0e3f?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop'
        ],
        
        # Annapodi (Rice Flour)
        'annapodi': [
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop'
        ],
        
        # Dhoop sticks
        'dhoop': [
            'https://images.unsplash.com/photo-1602928321679-711a8c0c0e3f?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop'
        ],
        
        # Dry Graphs (Dried Fruits)
        'dry_graphs': [
            'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1601493700631-2aade1f5b4a9?w=400&h=400&fit=crop'
        ],
        
        # Dry Nuts
        'dry_nuts': [
            'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=400&h=400&fit=crop'
        ],
        
        # Flakes
        'flakes': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Honey
        'honey': [
            'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&h=400&fit=crop'
        ],
        
        # Maavu (Flour)
        'maavu': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Malt
        'malt': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Masala (Spices)
        'masala': [
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop'
        ],
        
        # Millet
        'millet': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Noodles
        'noodles': [
            'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop'
        ],
        
        # Nuts and Seeds
        'nuts_seeds': [
            'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=400&h=400&fit=crop'
        ],
        
        # Oil
        'oil': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Paruppu (Lentils)
        'paruppu': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Payiru (Green Gram)
        'payiru': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Rasapodi
        'rasapodi': [
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop'
        ],
        
        # Rice
        'rice': [
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'
        ],
        
        # Rock Salt
        'rock_salt': [
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop'
        ],
        
        # Soap
        'soap': [
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop'
        ],
        
        # Soup
        'soup': [
            'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop'
        ],
        
        # Spices
        'spices': [
            'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop'
        ],
        
        # Tea
        'tea': [
            'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=400&fit=crop'
        ],
        
        # Single Products
        'digestive_bites': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&h=400&fit=crop',
        'dish_wash': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
        'femi9_pad': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
        'floor_cleaner': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
        'ghee': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&h=400&fit=crop',
        'health_mix': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
        'karuppu_kavuni': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
        'karuppu_kollu': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
        'karuppu_sundal': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
        'karuppu_ulundu': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop',
        'kunkumam': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
        'manjal': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop',
        'mosquito_coil': 'https://images.unsplash.com/photo-1602928321679-711a8c0c0e3f?w=400&h=400&fit=crop',
    }

def get_image_for_product(product):
    """Get appropriate image URL for a product"""
    image_urls = get_image_urls()
    
    # Check for single products first
    product_title_lower = product.title.lower()
    
    # Single products mapping
    single_product_mapping = {
        'digestive bites': 'digestive_bites',
        'dish wash powder': 'dish_wash',
        'femi9 pad': 'femi9_pad',
        'floor cleaner': 'floor_cleaner',
        'ghee': 'ghee',
        'health mix': 'health_mix',
        'karuppu kavuni kanji powder': 'karuppu_kavuni',
        'karuppu kollu': 'karuppu_kollu',
        'karuppu sundal': 'karuppu_sundal',
        'karuppu ulundu kanji powder': 'karuppu_ulundu',
        'kunkumam': 'kunkumam',
        'manjal': 'manjal',
        'mosquito coil': 'mosquito_coil',
    }
    
    # Check if it's a single product
    for key, value in single_product_mapping.items():
        if key in product_title_lower:
            return image_urls.get(value)
    
    # If it's a category product, use category-based images
    if product.category:
        category_name_lower = product.category.name.lower().replace(' ', '_')
        
        # Map category names to image keys
        category_mapping = {
            'agarbathi': 'agarbathi',
            'annapodi': 'annapodi',
            'dhoop sticks': 'dhoop',
            'dry graphs': 'dry_graphs',
            'dry nuts': 'dry_nuts',
            'flakes': 'flakes',
            'honey': 'honey',
            'maavu': 'maavu',
            'malt': 'malt',
            'masala': 'masala',
            'millet': 'millet',
            'noodles': 'noodles',
            'nuts and seeds': 'nuts_seeds',
            'oil': 'oil',
            'paruppu': 'paruppu',
            'payiru': 'payiru',
            'rasapodi': 'rasapodi',
            'rice': 'rice',
            'rock salt': 'rock_salt',
            'soap': 'soap',
            'soup': 'soup',
            'spices': 'spices',
            'tea': 'tea',
        }
        
        image_key = category_mapping.get(category_name_lower)
        if image_key and image_key in image_urls:
            urls = image_urls[image_key]
            if isinstance(urls, list):
                # Use product ID to select from multiple images
                return urls[product.id % len(urls)]
            return urls
    
    # Default image if no match found
    return 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop'

def add_images_to_products():
    """Add images to all products"""
    print("🖼️  Adding images to products...")
    print("=" * 50)
    
    products = Product.objects.all()
    total_products = products.count()
    updated_count = 0
    failed_count = 0
    
    for i, product in enumerate(products, 1):
        print(f"Processing {i}/{total_products}: {product.title}")
        
        # Skip if product already has an image
        if product.image:
            print(f"  ⏭️  Already has image: {product.image}")
            continue
        
        # Get appropriate image URL
        image_url = get_image_for_product(product)
        
        if not image_url:
            print(f"  ❌ No image URL found for: {product.title}")
            failed_count += 1
            continue
        
        # Generate filename
        product_name_safe = "".join(c for c in product.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        product_name_safe = product_name_safe.replace(' ', '_').lower()
        filename = f"{product.id}_{product_name_safe}.jpg"
        
        # Download and save image
        image_path = download_image(image_url, filename)
        
        if image_path:
            # Update product with image
            product.image = image_path
            product.save()
            print(f"  ✅ Added image: {image_path}")
            updated_count += 1
        else:
            print(f"  ❌ Failed to add image for: {product.title}")
            failed_count += 1
    
    print("=" * 50)
    print(f"📊 SUMMARY:")
    print(f"   Total products: {total_products}")
    print(f"   Updated: {updated_count}")
    print(f"   Failed: {failed_count}")
    print(f"   Already had images: {total_products - updated_count - failed_count}")
    print("=" * 50)
    
    return updated_count, failed_count

def main():
    """Main function to add images to products"""
    print("🚀 Starting product image addition...")
    print("=" * 50)
    
    # Check if requests is available
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library not found.")
        print("Please install it with: pip install requests")
        return
    
    # Add images to products
    updated, failed = add_images_to_products()
    
    if updated > 0:
        print(f"🎉 Successfully added images to {updated} products!")
    else:
        print("⚠️  No new images were added.")
    
    if failed > 0:
        print(f"⚠️  Failed to add images to {failed} products.")
    
    print("=" * 50)
    print("✅ Image addition process completed!")

if __name__ == "__main__":
    main() 