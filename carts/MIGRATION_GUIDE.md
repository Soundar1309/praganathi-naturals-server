# Rails to Django Migration Guide

This guide provides step-by-step instructions for migrating from the Ruby on Rails ecommerce application to the Django equivalent.

## Overview

The Django application is designed as a drop-in replacement for the Rails backend, preserving:
- All API endpoints and response formats
- Database schema and relationships
- Business logic and validation rules
- Authentication flow with JWT tokens
- Role-based access control

## Prerequisites

Before starting the migration:

1. **Backup your Rails database**
   ```bash
   pg_dump server_development > rails_backup.sql
   ```

2. **Document current API usage**
   - List all API endpoints used by your frontend
   - Note any custom response formats
   - Document authentication flow

3. **Prepare environment**
   - Install Python 3.11+
   - Install PostgreSQL
   - Install Redis (for background jobs)

## Migration Steps

### Step 1: Set Up Django Environment

1. **Clone the Django application**
   ```bash
   git clone <django-repo-url>
   cd ecommerce
   ```

2. **Run the setup script**
   ```bash
   ./setup.sh
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

### Step 2: Database Migration

1. **Create Django database**
   ```bash
   createdb ecommerce_development
   ```

2. **Run Django migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Step 3: Data Migration (Optional)

If you want to migrate existing data from Rails:

1. **Export Rails data to JSON**
   ```ruby
   # In Rails console
   require 'json'
   
   # Export users
   users = User.all.map(&:attributes)
   File.write('users.json', users.to_json)
   
   # Export categories
   categories = Category.all.map(&:attributes)
   File.write('categories.json', categories.to_json)
   
   # Export products
   products = Product.all.map(&:attributes)
   File.write('products.json', products.to_json)
   
   # Export orders
   orders = Order.all.map(&:attributes)
   File.write('orders.json', orders.to_json)
   ```

2. **Create Django management command for data import**
   ```python
   # Create file: users/management/commands/import_data.py
   from django.core.management.base import BaseCommand
   import json
   from users.models import User
   from products.models import Category, Product
   from orders.models import Order
   
   class Command(BaseCommand):
       help = 'Import data from Rails JSON exports'
       
       def handle(self, *args, **options):
           # Import users
           with open('users.json', 'r') as f:
               users_data = json.load(f)
               for user_data in users_data:
                   User.objects.create(**user_data)
           
           # Import categories
           with open('categories.json', 'r') as f:
               categories_data = json.load(f)
               for category_data in categories_data:
                   Category.objects.create(**category_data)
           
           # Continue for other models...
   ```

3. **Run data import**
   ```bash
   python manage.py import_data
   ```

### Step 4: Update Frontend Configuration

1. **Update API base URL** (if different)
   ```javascript
   // Update your frontend API configuration
   const API_BASE_URL = 'http://localhost:8000/api/';
   ```

2. **Verify authentication flow**
   - Test user registration
   - Test login/logout
   - Verify JWT token handling

3. **Test all API endpoints**
   - Products and categories
   - Shopping cart operations
   - Order management
   - Notifications

### Step 5: Background Jobs Setup

1. **Start Redis server**
   ```bash
   redis-server
   ```

2. **Start Celery worker**
   ```bash
   celery -A ecommerce worker -l info
   ```

3. **Test background jobs**
   - Order status change emails
   - Delivery assignment notifications
   - Cart cleanup tasks

### Step 6: Testing and Validation

1. **Run Django tests**
   ```bash
   python manage.py test
   ```

2. **API endpoint testing**
   ```bash
   # Test authentication
   curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123","password_confirmation":"password123"}'
   
   # Test products endpoint
   curl http://localhost:8000/api/products/
   
   # Test protected endpoints
   curl -H "Authorization: Bearer <token>" http://localhost:8000/api/profile/
   ```

3. **Frontend integration testing**
   - Test all user flows
   - Verify data consistency
   - Check error handling

## API Endpoint Mapping

| Rails Endpoint | Django Endpoint | Notes |
|----------------|-----------------|-------|
| `POST /login` | `POST /api/login/` | Same request/response format |
| `DELETE /logout` | `DELETE /api/logout/` | Same request/response format |
| `GET /profile` | `GET /api/profile/` | Same response format |
| `PUT /profile` | `PUT /api/profile/update/` | Same request/response format |
| `GET /products` | `GET /api/products/` | Same query parameters |
| `POST /products` | `POST /api/products/` | Admin only, same format |
| `GET /categories` | `GET /api/categories/` | Same response format |
| `GET /carts` | `GET /api/carts/` | Same response format |
| `POST /cart_items` | `POST /api/cart_items/` | Same request/response format |
| `GET /orders` | `GET /api/orders/` | Same response format |
| `POST /orders` | `POST /api/orders/` | Same request/response format |
| `GET /notifications` | `GET /api/notifications/` | Same response format |

## Key Differences

### Authentication
- **Rails**: Devise with JWT
- **Django**: djangorestframework-simplejwt
- **Migration**: Same JWT token format, no changes needed

### Database
- **Rails**: ActiveRecord with PostgreSQL
- **Django**: Django ORM with PostgreSQL
- **Migration**: Same schema, same relationships

### Background Jobs
- **Rails**: ActiveJob with Sidekiq/Resque
- **Django**: Celery with Redis
- **Migration**: Same job functionality, different implementation

### File Uploads
- **Rails**: Active Storage
- **Django**: Django File Storage
- **Migration**: Same upload endpoints, same file handling

## Troubleshooting

### Common Issues

1. **Database connection errors**
   ```bash
   # Check PostgreSQL is running
   sudo systemctl status postgresql
   
   # Check database exists
   psql -l | grep ecommerce
   ```

2. **Migration errors**
   ```bash
   # Reset migrations if needed
   python manage.py migrate --fake-initial
   
   # Check migration status
   python manage.py showmigrations
   ```

3. **Authentication issues**
   ```bash
   # Check JWT settings
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.SIMPLE_JWT)
   ```

4. **Background job issues**
   ```bash
   # Check Redis connection
   redis-cli ping
   
   # Check Celery worker
   celery -A ecommerce inspect active
   ```

### Performance Optimization

1. **Database optimization**
   ```python
   # Use select_related and prefetch_related
   products = Product.objects.select_related('category').all()
   orders = Order.objects.prefetch_related('order_items__product').all()
   ```

2. **Caching**
   ```python
   # Add Redis caching
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

3. **Static files**
   ```bash
   # Collect static files for production
   python manage.py collectstatic
   ```

## Production Deployment

1. **Environment setup**
   ```bash
   # Set production environment variables
   export DEBUG=False
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=postgres://user:pass@host:port/db
   ```

2. **Database setup**
   ```bash
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

3. **Static files**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   ```

4. **Start services**
   ```bash
   # Start Gunicorn
   gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
   
   # Start Celery worker
   celery -A ecommerce worker -l info
   
   # Start Celery beat (for scheduled tasks)
   celery -A ecommerce beat -l info
   ```

## Rollback Plan

If issues arise during migration:

1. **Keep Rails application running** during migration
2. **Use feature flags** to switch between backends
3. **Monitor API responses** for differences
4. **Have database backup** ready for rollback

## Support

For migration assistance:
1. Check the Django documentation
2. Review the API documentation
3. Test thoroughly in staging environment
4. Monitor application logs for errors

## Conclusion

The Django application provides a complete replacement for the Rails backend with:
- Identical API functionality
- Same database schema
- Equivalent business logic
- Compatible authentication
- Production-ready deployment

The migration should be transparent to your frontend application, requiring minimal or no changes to existing code. 