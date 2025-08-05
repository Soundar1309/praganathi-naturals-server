# How to Run Django Backend

## 🚀 **Quick Start (3 Ways)**

### **Method 1: One-Liner Script (Easiest)**
```bash
cd backend
./start.sh
```

### **Method 2: Server Control Script**
```bash
cd backend
source venv/bin/activate
python3 server_control.py start
```

### **Method 3: Manual Start**
```bash
cd backend
source venv/bin/activate
python3 manage.py runserver
```

## 🎮 **Server Management**

### **Check Status**
```bash
python3 server_control.py status
```

### **Stop Server**
```bash
python3 server_control.py stop
```

### **Restart Server**
```bash
python3 server_control.py restart
```

## 📍 **Access Your Application**

Once running, access:

- **🌐 Main URL**: http://localhost:8000/
- **📱 API Base**: http://localhost:8000/api/
- **🔧 Admin Panel**: http://localhost:8000/admin/
- **💚 Health Check**: http://localhost:8000/up/

### **Admin Login**
- **Email**: admin@ecommerce.com
- **Password**: admin123

## 🧪 **Test Your API**

### **Health Check**
```bash
curl http://localhost:8000/up/
```

### **Register User**
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

### **Login**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## 📋 **Available Endpoints**

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

## ✅ **Current Status**

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

## 🚨 **Troubleshooting**

### **Port Already in Use**
```bash
python3 server_control.py stop
python3 server_control.py start
```

### **Virtual Environment Not Activated**
```bash
source venv/bin/activate
```

### **Database Connection Issues**
Check your `.env` file and ensure PostgreSQL is running.

**Your Django ecommerce backend is ready to use! 🚀** 