# Django Ecommerce Backend

A Django REST API backend for the ecommerce application, converted from Ruby on Rails.

## Quick Start

1. **Setup Virtual Environment**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Setup Environment**
   ```bash
   cp ../env.example .env
   # Edit .env with your database credentials
   ```

4. **Create Database**
   ```bash
   createdb ecommerce_development
   ```

5. **Run Migrations**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python3 create_superuser.py
   ```

7. **Start Server**
   ```bash
   python3 manage.py runserver
   ```

## Alternative: Use the Run Script

```bash
cd backend
source venv/bin/activate
python3 run_backend.py
```

## Access Points

- **API Base URL**: http://localhost:8000/api/
- **Admin Interface**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/up/

### Admin Credentials
- Email: admin@ecommerce.com
- Password: admin123

## API Endpoints

### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `DELETE /api/logout/` - User logout

### Products
- `GET /api/products/` - List products
- `POST /api/products/` - Create product (admin only)

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category

### Cart
- `GET /api/carts/` - Get user cart
- `POST /api/cart_items/` - Add item to cart

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order

### Notifications
- `GET /api/notifications/` - List notifications

## Testing the API

### Register a User
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "password_confirmation": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## Features

- JWT Authentication with role-based access control
- RESTful API with Django REST Framework
- PostgreSQL Database with Django ORM
- Background Jobs with Celery (optional)
- Admin Interface for data management
- CORS Support for frontend integration
- File Upload for product images
- Email Notifications for order updates

## Migration from Rails

This Django application is designed to be a **drop-in replacement** for the Rails backend with the same API endpoints and response formats. 