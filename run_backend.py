#!/usr/bin/env python3
"""
Django Ecommerce Backend Runner
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_virtual_environment():
    """Check if virtual environment is activated"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️ Virtual environment not detected")
        print("Please activate the virtual environment: source venv/bin/activate")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import django
        import rest_framework
        import psycopg2
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r ../requirements.txt")
        return False

def check_database():
    """Check if database is accessible"""
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
        django.setup()
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your database settings in .env file")
        return False

def setup_environment():
    """Set up environment variables"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        if os.path.exists('../env.example'):
            subprocess.run(['cp', '../env.example', '.env'])
            print("✅ .env file created")
        else:
            print("⚠️ No env.example found, please create .env manually")
    else:
        print("✅ .env file exists")

def run_migrations():
    """Run database migrations"""
    print("🔄 Running migrations...")
    try:
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True, check=True)
        print("✅ Migrations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e.stderr}")
        return False

def create_superuser_if_needed():
    """Create superuser if it doesn't exist"""
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
        django.setup()
        
        from users.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("🔄 Creating superuser...")
            subprocess.run([sys.executable, 'create_superuser.py'], check=True)
        else:
            print("✅ Superuser already exists")
        return True
    except Exception as e:
        print(f"⚠️ Could not check/create superuser: {e}")
        return True

def run_django():
    """Run Django development server"""
    print("\n🚀 Starting Django development server...")
    print("📱 API will be available at: http://localhost:8000/api/")
    print("🔧 Admin interface at: http://localhost:8000/admin/")
    print("💚 Health check at: http://localhost:8000/up/")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    print("🎯 Django Ecommerce Backend Runner")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check virtual environment
    if not check_virtual_environment():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    setup_environment()
    
    # Check database
    if not check_database():
        return
    
    # Run migrations
    if not run_migrations():
        return
    
    # Create superuser if needed
    create_superuser_if_needed()
    
    # Run Django
    run_django()

if __name__ == "__main__":
    main() 