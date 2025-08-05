# 🚀 Django Backend Running Guide

## ✅ **Current Status: RUNNING**

Your Django backend is **successfully running** on:
- **🌐 Main URL**: http://localhost:8000/
- **📱 API Base**: http://localhost:8000/api/
- **🔧 Admin Panel**: http://localhost:8000/admin/
- **💚 Health Check**: http://localhost:8000/up/ ✅

## 🛠️ **How to Run the Backend**

### **Method 1: Quick Start (Recommended)**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend
./start.sh
```

### **Method 2: Comprehensive Runner**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend
python3 run_backend.py
```

### **Method 3: Server Control Script**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend

# Check status
python3 server_control.py status

# Start server
python3 server_control.py start

# Stop server
python3 server_control.py stop

# Restart server
python3 server_control.py restart
```

### **Method 4: Manual Django Commands**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend

# Activate virtual environment
source venv/bin/activate

# Run migrations (if needed)
python3 manage.py migrate

# Start server
python3 manage.py runserver
```

## 🧪 **Test Your Backend**

### **Health Check**
```bash
curl http://localhost:8000/up/
# Should return: OK
```

### **API Test**
```bash
curl http://localhost:8000/api/products/
# Should return JSON with products
```

### **Admin Panel**
Visit: http://localhost:8000/admin/
- **Email**: admin@ecommerce.com
- **Password**: admin123

## 📋 **Available Endpoints**

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/up/` | GET | Health check | ✅ Working |
| `/api/register/` | POST | User registration | ✅ Working |
| `/api/login/` | POST | User login | ✅ Working |
| `/api/logout/` | DELETE | User logout | ✅ Working |
| `/api/profile/` | GET | Get user profile | ✅ Working |
| `/api/products/` | GET | List products | ✅ Working |
| `/api/categories/` | GET | List categories | ✅ Working |
| `/api/carts/` | GET | Get user cart | ✅ Working |
| `/api/orders/` | GET | List orders | ✅ Working |
| `/api/notifications/` | GET | List notifications | ✅ Working |

## 🔧 **Troubleshooting**

### **Port Already in Use**
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use server control
python3 server_control.py stop
python3 server_control.py start
```

### **Virtual Environment Issues**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Database Issues**
```bash
# Reset database
python3 manage.py flush

# Run migrations
python3 manage.py migrate

# Create superuser
python3 create_superuser.py
```

### **Permission Issues**
```bash
# Make scripts executable
chmod +x start.sh
chmod +x server_control.py
```

## 🎯 **Quick Commands**

### **Start Backend**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend && ./start.sh
```

### **Stop Backend**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend && python3 server_control.py stop
```

### **Restart Backend**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend && python3 server_control.py restart
```

### **Check Status**
```bash
cd /home/sasikalavijayakumar/ecommerce/backend && python3 server_control.py status
```

## 📱 **Frontend Integration**

Your React frontend is configured to connect to:
- **API URL**: http://localhost:8000/api
- **CORS**: Configured for port 5173 ✅

## 🎉 **Ready to Use**

Your Django backend is **fully operational** and ready for:
- ✅ **User registration and login**
- ✅ **Product browsing**
- ✅ **Shopping cart functionality**
- ✅ **Order management**
- ✅ **Admin panel access**

**Start building your ecommerce application! 🚀** 