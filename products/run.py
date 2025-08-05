#!/usr/bin/env python3
"""
Simple script to run the Django ecommerce application
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

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
        print("Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up environment variables"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        if os.path.exists('env.example'):
            subprocess.run(['cp', 'env.example', '.env'])
            print("✅ .env file created")
        else:
            print("⚠️ No env.example found, please create .env manually")
    else:
        print("✅ .env file exists")

def run_django():
    """Run Django development server"""
    print("🚀 Starting Django development server...")
    print("📱 API will be available at: http://localhost:8000/api/")
    print("🔧 Admin interface at: http://localhost:8000/admin/")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    print("🎯 Django Ecommerce Application Runner")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    setup_environment()
    
    # Run Django
    run_django()

if __name__ == "__main__":
    main() 