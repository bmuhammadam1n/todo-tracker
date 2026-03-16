#!/bin/bash
set -e

echo "🔧 Starting build..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "🗂️ Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Create superuser (optional, for demo)
echo "👤 Creating superuser (if not exists)..."
python create_superuser.py || echo "⚠️ Superuser creation skipped"

echo "✅ Build complete!"