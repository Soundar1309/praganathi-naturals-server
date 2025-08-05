#!/bin/bash

# Ecommerce Django Setup Script

echo "🚀 Setting up Ecommerce Django Application..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp env.example .env
    echo "📝 Please edit .env file with your configuration"
fi

# Check if PostgreSQL is running
echo "🗄️ Checking PostgreSQL connection..."
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️ PostgreSQL is not running. Please start PostgreSQL and try again."
    echo "💡 You can start PostgreSQL with: sudo systemctl start postgresql"
    exit 1
fi

# Create database if it doesn't exist
echo "🗄️ Creating database..."
createdb ecommerce_development 2>/dev/null || echo "Database already exists"

# Run migrations
echo "🔄 Running migrations..."
python manage.py makemigrations users
python manage.py makemigrations products
python manage.py makemigrations carts
python manage.py makemigrations orders
python manage.py makemigrations notifications
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
echo "Please create a superuser account:"
python manage.py createsuperuser

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Start the development server: python manage.py runserver"
echo "2. Start Celery worker: celery -A ecommerce worker -l info"
echo "3. Access the API at: http://localhost:8000/api/"
echo "4. Access admin at: http://localhost:8000/admin/"
echo ""
echo "📚 For more information, see README.md" 