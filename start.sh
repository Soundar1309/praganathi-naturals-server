#!/bin/bash

# Django Ecommerce Backend Starter Script

echo "🚀 Starting Django Ecommerce Backend..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️ Virtual environment not detected"
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if server is already running
if python3 server_control.py status > /dev/null 2>&1; then
    echo "✅ Server is already running!"
    echo "   URL: http://localhost:8000/"
    echo "   API: http://localhost:8000/api/"
    echo "   Admin: http://localhost:8000/admin/"
    exit 0
fi

# Start the server
python3 server_control.py start

echo ""
echo "🎉 Django server is ready!"
echo "📱 API: http://localhost:8000/api/"
echo "🔧 Admin: http://localhost:8000/admin/ (admin@ecommerce.com / admin123)"
echo "🛑 To stop: python3 server_control.py stop" 