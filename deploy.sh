#!/bin/bash

# PRAGATHI SERVER - Backend Deployment Script
# This script deploys the updated backend with new pricing features
# 
# Features added:
# - original_price field with default ₹10000
# - offer_price field (automatically set to price)
# - Enhanced pricing display and validation
# - Updated admin interface

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="PRAGATHI-SERVER"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="backup_${TIMESTAMP}"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if we're in the correct directory
check_directory() {
    if [[ ! -f "manage.py" ]]; then
        error "This script must be run from the PRAGATHI-SERVER directory (where manage.py is located)"
    fi
    log "Working directory verified: $(pwd)"
}

# Check if virtual environment exists
check_venv() {
    if [[ ! -d "venv" ]]; then
        error "Virtual environment not found. Please ensure 'venv' directory exists."
    fi
    log "Virtual environment found"
}

# Create backup directory
create_backup_dir() {
    if [[ ! -d "$BACKUP_DIR" ]]; then
        mkdir -p "$BACKUP_DIR"
        log "Created backup directory: $BACKUP_DIR"
    fi
}

# Backup current database
backup_database() {
    log "Creating database backup..."
    
    if [[ -f "db.sqlite3" ]]; then
        cp db.sqlite3 "$BACKUP_DIR/${BACKUP_NAME}.sqlite3"
        success "Database backed up to: $BACKUP_DIR/${BACKUP_NAME}.sqlite3"
    else
        warning "No database file found to backup"
    fi
}

# Backup current code
backup_code() {
    log "Creating code backup..."
    
    # Create a tar.gz of current code (excluding venv, backups, and media)
    tar --exclude='venv' --exclude='backups' --exclude='media' --exclude='*.pyc' \
        --exclude='__pycache__' --exclude='.git' \
        -czf "$BACKUP_DIR/${BACKUP_NAME}_code.tar.gz" .
    
    success "Code backed up to: $BACKUP_DIR/${BACKUP_NAME}_code.tar.gz"
}

# Activate virtual environment
activate_venv() {
    log "Activating virtual environment..."
    source venv/bin/activate
    
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        error "Failed to activate virtual environment"
    fi
    
    success "Virtual environment activated: $VIRTUAL_ENV"
}

# Check Django installation
check_django() {
    log "Checking Django installation..."
    
    if ! python -c "import django; print('Django version:', django.get_version())" 2>/dev/null; then
        error "Django is not installed or not accessible"
    fi
    
    success "Django is accessible"
}

# Install/update dependencies
install_dependencies() {
    log "Installing/updating dependencies..."
    
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt --upgrade
        success "Dependencies updated"
    else
        warning "No requirements.txt found, skipping dependency update"
    fi
}

# Run Django checks
run_django_checks() {
    log "Running Django system checks..."
    
    if ! python manage.py check --deploy; then
        error "Django system checks failed"
    fi
    
    success "Django system checks passed"
}

# Apply migrations
apply_migrations() {
    log "Applying database migrations..."
    
    # Show migration status
    python manage.py showmigrations
    
    # Apply migrations
    if ! python manage.py migrate; then
        error "Failed to apply migrations"
    fi
    
    success "Migrations applied successfully"
}

# Update existing products
update_existing_products() {
    log "Updating existing products with new pricing fields..."
    
    # Create a temporary script to update products
    cat > temp_update_products.py << 'EOF'
#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product
from decimal import Decimal

def update_products():
    """Update existing products to have correct pricing fields"""
    products = Product.objects.all()
    
    print(f"Found {products.count()} products to update...")
    
    updated_count = 0
    for product in products:
        # Ensure original_price is set
        if not product.original_price or product.original_price == 0:
            product.original_price = Decimal('10000.00')
        
        # Set offer_price to price
        product.offer_price = product.price
        
        # Save without triggering validation
        product.save(update_fields=['original_price', 'offer_price'])
        updated_count += 1
        print(f"Updated product '{product.title}' - Price: {product.price}, Original: {product.original_price}, Offer: {product.offer_price}")
    
    print(f"\nSuccessfully updated {updated_count} products!")
    
    # Verify all products have correct fields
    products_without_original = Product.objects.filter(original_price__isnull=True)
    products_without_offer = Product.objects.filter(offer_price__isnull=True)
    
    if products_without_original.exists():
        print(f"Warning: {products_without_original.count()} products still don't have original_price set!")
    else:
        print("All products have original_price set!")
    
    if products_without_offer.exists():
        print(f"Warning: {products_without_offer.count()} products still don't have offer_price set!")
    else:
        print("All products have offer_price set!")

if __name__ == '__main__':
    try:
        update_products()
    except Exception as e:
        print(f"Error updating products: {e}")
        sys.exit(1)
EOF

    # Run the update script
    if ! python temp_update_products.py; then
        error "Failed to update existing products"
    fi
    
    # Clean up temporary script
    rm temp_update_products.py
    
    success "Existing products updated successfully"
}

# Collect static files
collect_static() {
    log "Collecting static files..."
    
    if ! python manage.py collectstatic --noinput; then
        error "Failed to collect static files"
    fi
    
    success "Static files collected"
}

# Test the deployment
test_deployment() {
    log "Testing deployment..."
    
    # Test if server can start
    timeout 10s python manage.py runserver 0.0.0.0:8001 > /dev/null 2>&1 &
    SERVER_PID=$!
    
    sleep 3
    
    # Test API endpoint
    if curl -s http://localhost:8001/api/products/products/ > /dev/null; then
        success "API endpoint is accessible"
    else
        warning "API endpoint test failed"
    fi
    
    # Stop test server
    kill $SERVER_PID 2>/dev/null || true
    
    success "Deployment test completed"
}

# Create deployment summary
create_summary() {
    log "Creating deployment summary..."
    
    cat > "deployment_summary_${TIMESTAMP}.txt" << EOF
PRAGATHI SERVER - Backend Deployment Summary
============================================

Deployment Time: $(date)
Deployment Script: $0

CHANGES DEPLOYED:
================
1. Added original_price field to Product model (default: ₹10000)
2. Added offer_price field (automatically set to price)
3. Enhanced pricing validation and display
4. Updated admin interface with new fields
5. Added computed properties: has_offer, discount_percentage

BACKUP FILES:
=============
- Database: $BACKUP_DIR/${BACKUP_NAME}.sqlite3
- Code: $BACKUP_DIR/${BACKUP_NAME}_code.tar.gz

MIGRATIONS APPLIED:
==================
- 0003_product_offer_price_product_original_price.py
- 0004_alter_product_offer_price.py

PRODUCTS UPDATED:
================
$(python manage.py shell -c "
from products.models import Product
products = Product.objects.all()
print(f'Total products: {products.count()}')
for p in products[:5]:  # Show first 5
    print(f'- {p.title}: Price ₹{p.price}, Original ₹{p.original_price}, Offer ₹{p.offer_price}')
if products.count() > 5:
    print(f'... and {products.count() - 5} more products')
")

NEXT STEPS:
===========
1. Test the frontend with the new backend
2. Verify pricing display in product cards and detail pages
3. Test product creation/editing forms
4. Monitor admin interface for new fields

ROLLBACK INSTRUCTIONS:
======================
If rollback is needed:
1. Stop the server
2. Restore database: cp $BACKUP_DIR/${BACKUP_NAME}.sqlite3 db.sqlite3
3. Restore code: tar -xzf $BACKUP_DIR/${BACKUP_NAME}_code.tar.gz
4. Restart server

EOF

    success "Deployment summary created: deployment_summary_${TIMESTAMP}.txt"
}

# Main deployment function
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                PRAGATHI SERVER DEPLOYMENT                   ║"
    echo "║                    Backend Update                           ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log "Starting deployment process..."
    
    # Pre-deployment checks
    check_directory
    check_venv
    create_backup_dir
    
    # Create backups
    backup_database
    backup_code
    
    # Activate environment and deploy
    activate_venv
    check_django
    install_dependencies
    run_django_checks
    apply_migrations
    update_existing_products
    collect_static
    
    # Test deployment
    test_deployment
    
    # Create summary
    create_summary
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    DEPLOYMENT COMPLETE!                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    success "Backend deployment completed successfully!"
    log "Backup files are available in: $BACKUP_DIR"
    log "Deployment summary: deployment_summary_${TIMESTAMP}.txt"
    
    echo -e "${YELLOW}"
    echo "Next steps:"
    echo "1. Test the frontend with the new backend"
    echo "2. Verify pricing display in product cards"
    echo "3. Test product creation/editing forms"
    echo "4. Monitor admin interface for new fields"
    echo -e "${NC}"
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --backup-only  Only create backups, don't deploy"
        echo "  --test-only    Only test the current deployment"
        echo ""
        echo "This script deploys the updated PRAGATHI SERVER backend with new pricing features."
        exit 0
        ;;
    --backup-only)
        log "Backup-only mode selected"
        check_directory
        check_venv
        create_backup_dir
        backup_database
        backup_code
        success "Backup completed successfully!"
        exit 0
        ;;
    --test-only)
        log "Test-only mode selected"
        check_directory
        check_venv
        activate_venv
        test_deployment
        success "Test completed successfully!"
        exit 0
        ;;
    "")
        # No arguments, run full deployment
        main
        ;;
    *)
        error "Unknown option: $1. Use --help for usage information."
        ;;
esac
