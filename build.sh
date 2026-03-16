#!/bin/bash
set -e

echo "🚀 Starting Render build..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "🗂️ Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser for demo (optional)
echo "👤 Creating demo superuser..."
python create_superuser.py || echo "⚠️ Superuser creation skipped (may already exist)"

echo "✅ Build completed successfully!"