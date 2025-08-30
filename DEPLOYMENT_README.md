# PRAGATHI SERVER - Backend Deployment Guide

This guide explains how to deploy the updated backend with new pricing features.

## 🚀 New Features Deployed

- **original_price field**: Default ₹10000, shown with strikethrough when there's an offer
- **offer_price field**: Automatically set to the same value as price
- **Enhanced pricing display**: Shows discount percentages and offer badges
- **Updated admin interface**: New fields organized in logical groups
- **Automatic validation**: Ensures price < original_price for offers

## 📁 Deployment Scripts

### 1. Full Deployment Script (`deploy.sh`)

**Use this for:**
- Production deployments
- When you want full backups and comprehensive testing
- First-time deployment of the pricing features

**Features:**
- ✅ Creates database and code backups
- ✅ Comprehensive error checking
- ✅ Tests deployment before completion
- ✅ Creates detailed deployment summary
- ✅ Handles rollback instructions

**Usage:**
```bash
# Full deployment
./deploy.sh

# Only create backups
./deploy.sh --backup-only

# Only test current deployment
./deploy.sh --test-only

# Show help
./deploy.sh --help
```

### 2. Quick Deployment Script (`quick_deploy.sh`)

**Use this for:**
- Development/testing environments
- When you need rapid deployment
- Updates to existing deployments

**Features:**
- ✅ Fast deployment (no backups)
- ✅ Applies migrations
- ✅ Updates existing products
- ✅ Basic testing
- ✅ Shows deployment status

**Usage:**
```bash
./quick_deploy.sh
```

## 🔧 Pre-Deployment Requirements

1. **Environment**: Must be in PRAGATHI-SERVER directory
2. **Virtual Environment**: `venv` directory must exist
3. **Dependencies**: All requirements must be installed
4. **Permissions**: Scripts must be executable

## 📋 Deployment Steps

### Step 1: Navigate to Project Directory
```bash
cd /path/to/PRAGATHI-SERVER
```

### Step 2: Make Scripts Executable (if needed)
```bash
chmod +x deploy.sh
chmod +x quick_deploy.sh
```

### Step 3: Run Deployment
```bash
# For production/full deployment
./deploy.sh

# For quick deployment
./quick_deploy.sh
```

## 🔍 What Happens During Deployment

### Full Deployment (`deploy.sh`)
1. **Pre-deployment Checks**
   - Verifies working directory
   - Checks virtual environment
   - Creates backup directories

2. **Backup Creation**
   - Database backup (`backup_YYYYMMDD_HHMMSS.sqlite3`)
   - Code backup (`backup_YYYYMMDD_HHMMSS_code.tar.gz`)

3. **Environment Setup**
   - Activates virtual environment
   - Checks Django installation
   - Updates dependencies

4. **Database Updates**
   - Runs Django system checks
   - Applies migrations
   - Updates existing products

5. **Finalization**
   - Collects static files
   - Tests deployment
   - Creates deployment summary

### Quick Deployment (`quick_deploy.sh`)
1. **Environment Check**
2. **Apply Migrations**
3. **Update Products**
4. **Collect Static Files**
5. **Test Deployment**

## 📊 Post-Deployment Verification

### 1. Check API Endpoints
```bash
curl http://localhost:8000/api/products/products/ | python -m json.tool | head -20
```

**Expected Response:**
```json
{
  "results": [
    {
      "id": 1,
      "title": "iPhone 15 Pro",
      "price": "999.99",
      "original_price": "10000.00",
      "offer_price": "999.99",
      "has_offer": true,
      "discount_percentage": 90.0
    }
  ]
}
```

### 2. Check Admin Interface
- Navigate to `/admin/products/product/`
- Verify new fields are visible
- Check that products show correct pricing

### 3. Test Frontend
- Verify product cards show strikethrough prices
- Check discount badges appear
- Test product creation/editing forms

## 🚨 Troubleshooting

### Common Issues

**1. Permission Denied**
```bash
chmod +x deploy.sh
chmod +x quick_deploy.sh
```

**2. Virtual Environment Not Found**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Migration Errors**
```bash
# Check migration status
python manage.py showmigrations

# Reset migrations if needed
python manage.py migrate products zero
python manage.py migrate
```

**4. Database Locked**
```bash
# Stop any running Django processes
pkill -f "python manage.py runserver"
```

### Rollback Instructions

If deployment fails or you need to rollback:

1. **Stop the server**
2. **Restore database:**
   ```bash
   cp backups/backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
   ```
3. **Restore code:**
   ```bash
   tar -xzf backups/backup_YYYYMMDD_HHMMSS_code.tar.gz
   ```
4. **Restart server**

## 📈 Monitoring

### Check Deployment Status
```bash
# View recent deployment summaries
ls -la deployment_summary_*.txt

# Check backup files
ls -la backups/
```

### Monitor Products
```bash
# Check products with offers
python manage.py shell -c "
from products.models import Product
offers = Product.objects.filter(original_price__gt=models.F('price'))
print(f'Products with offers: {offers.count()}')
for p in offers[:3]:
    print(f'- {p.title}: ₹{p.price} (was ₹{p.original_price})')
"
```

## 🔗 Related Files

- **Models**: `products/models.py`
- **Serializers**: `products/serializers.py`
- **Admin**: `products/admin.py`
- **Migrations**: `products/migrations/`
- **Frontend**: `../PRAGATHI-UI/`

## 📞 Support

If you encounter issues:

1. Check the deployment logs
2. Verify all requirements are met
3. Check the troubleshooting section
4. Review the deployment summary file

---

**Last Updated**: $(date)
**Version**: 1.0
**Features**: Pricing System Enhancement
