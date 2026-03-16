# config/settings_prod.py
from .settings import *
import dj_database_url
import os

# Security
DEBUG = False

# Allowed hosts (Render will set this)
ALLOWED_HOSTS = ['*']

# Secret key from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database (Render PostgreSQL)
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF Trusted Origins (for HTMX)
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]

# CSRF Cookie (needed for HTMX on production)
CSRF_COOKIE_HTTPONLY = False