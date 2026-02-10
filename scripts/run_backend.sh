#!/bin/bash
# Start Django backend - required for both web and desktop apps
cd "$(dirname "$0")/../backend"
echo "Initializing database..."
python manage.py migrate
echo ""
echo "Starting Django server on http://127.0.0.1:8000"
echo "Web app: http://localhost:3000"
echo "Desktop app: python desktop/main.py"
echo ""
python manage.py runserver
