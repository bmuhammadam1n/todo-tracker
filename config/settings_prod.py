# config/settings_prod.py
# Production settings for Render deployment

import os
import dj_database_url

# Import base settings first
from .settings import *

# =============================================================================
# SECURITY
# =============================================================================
DEBUG = False

# Allow all Render subdomains + custom domains
ALLOWED_HOSTS = ['*.onrender.com', 'onrender.com']

# Secret key from environment (required!)
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY environment variable is required")

# =============================================================================
# DATABASE (Render PostgreSQL)
# =============================================================================
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL environment variable is required")

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,  # Keep connections alive for 10 minutes
        conn_health_checks=True,  # Check connection health
    )
}

# =============================================================================
# STATIC FILES (WhiteNoise)
# =============================================================================
# Insert WhiteNoise middleware AFTER security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Add here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

# Static files configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================================
# SECURITY SETTINGS (Production)
# =============================================================================
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF trusted origins for HTMX on Render
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://onrender.com',
]

# HTMX needs CSRF cookie accessible to JavaScript
CSRF_COOKIE_HTTPONLY = False

# =============================================================================
# LOGGING (for debugging on Render)
# =============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =============================================================================
# EMAIL (Optional - for password reset, etc.)
# =============================================================================
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')