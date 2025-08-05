# Django Backend Quick Start

## 🚀 **Your Django Server is Running!**

The Django ecommerce backend is now successfully running and ready to use.

## 📍 **Access Points**

- **🌐 Main URL**: http://localhost:8000/
- **📱 API Base**: http://localhost:8000/api/
- **🔧 Admin Panel**: http://localhost:8000/admin/
- **💚 Health Check**: http://localhost:8000/up/

## 🔑 **Admin Login**

- **Email**: admin@ecommerce.com
- **Password**: admin123

## 🎮 **Server Control**

Use the server control script to manage the Django server:

```bash
# Check server status
python3 server_control.py status

# Start server
python3 server_control.py start

# Stop server
python3 server_control.py stop

# Restart server
python3 server_control.py restart
```

## 🧪 **Test the API**

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

## 📋 **Available API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register/` | POST | User registration |
| `/api/login/` | POST | User login |
| `/api/logout/` | DELETE | User logout |
| `/api/profile/` | GET | Get user profile |
| `/api/products/` | GET | List products |
| `/api/categories/` | GET | List categories |
| `/api/carts/` | GET | Get user cart |
| `/api/orders/` | GET | List orders |
| `/api/notifications/` | GET | List notifications |

## 🎯 **Next Steps**

1. **Explore Admin Panel**: Visit http://localhost:8000/admin/ to manage data
2. **Test API Endpoints**: Use curl or Postman to test the API
3. **Add Sample Data**: Create categories and products through admin
4. **Integrate Frontend**: Update your frontend to use the new API

## 🛠️ **Development Commands**

```bash
# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser
python3 create_superuser.py

# Django shell
python3 manage.py shell

# Run tests
python3 manage.py test
```

## ✅ **Status Check**

Your Django backend is:
- ✅ **Running** on http://localhost:8000
- ✅ **Database** connected and migrated
- ✅ **Admin user** created
- ✅ **All API endpoints** available
- ✅ **Ready for frontend integration**

## 🔄 **Rails Compatibility**

This Django backend is a **drop-in replacement** for your Rails backend:
- Same API endpoints and response formats
- Identical database schema
- Equivalent business logic
- Compatible with existing frontend

**Your Django ecommerce backend is ready to use! 🚀** 