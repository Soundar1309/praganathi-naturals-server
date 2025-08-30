#!/bin/bash

# PRAGATHI SERVER - Quick Deployment Script
# This script quickly deploys the pricing feature updates

set -e

echo "🚀 PRAGATHI SERVER - Quick Deployment"
echo "======================================"

# Check if we're in the right directory
if [[ ! -f "manage.py" ]]; then
    echo "❌ Error: This script must be run from the PRAGATHI-SERVER directory"
    exit 1
fi

# Check virtual environment
if [[ ! -d "venv" ]]; then
    echo "❌ Error: Virtual environment not found"
    exit 1
fi

echo "✅ Environment check passed"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Apply migrations
echo "📊 Applying database migrations..."
python manage.py migrate

# Update existing products
echo "🔄 Updating existing products..."
python manage.py shell -c "
from products.models import Product
from decimal import Decimal

products = Product.objects.all()
print(f'Updating {products.count()} products...')

for product in products:
    if not product.original_price or product.original_price == 0:
        product.original_price = Decimal('10000.00')
    product.offer_price = product.price
    product.save(update_fields=['original_price', 'offer_price'])

print('✅ All products updated successfully!')
"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Test deployment
echo "🧪 Testing deployment..."
python manage.py check --deploy

echo ""
echo "🎉 Quick deployment completed successfully!"
echo ""
echo "📋 What was deployed:"
echo "   • New pricing fields (original_price, offer_price)"
echo "   • Enhanced pricing validation"
echo "   • Updated admin interface"
echo "   • All existing products updated"
echo ""
echo "🔗 Next steps:"
echo "   1. Restart your Django server"
echo "   2. Test the frontend with new pricing display"
echo "   3. Verify admin interface shows new fields"
echo ""
echo "📊 Current products status:"
python manage.py shell -c "
from products.models import Product
from django.db import models

products = Product.objects.all()
print(f'Total products: {products.count()}')
offers = products.filter(original_price__gt=models.F('price')).count()
print(f'Products with offers: {offers}')
print(f'Products without offers: {products.count() - offers}')
"
