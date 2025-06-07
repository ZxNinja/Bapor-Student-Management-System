# sms_backend/settings.py
# This file contains the main configuration for your Django project.

import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Use environment variable for SECRET_KEY for security
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'slm$kz=tkjmztcjtke&vqh0-4)-@=$k57#oeaq@^r5sui)e%wa')

# Set DEBUG to False in production. Use environment variable.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

# Allowed hosts for your Django application.
# IMPORTANT: You need to add the hostname of your Render web service here.
# You can find this URL in your Render dashboard after deployment.
# It will look something like: your-service-name.onrender.com
# For initial deployment, it's common to use ['.render.com', 'your-custom-domain.com']
# Or simply '*' if you trust Render's security groups and want to avoid issues.
# For now, we'll keep '*' as a fallback, but specify your Render domain.
ALLOWED_HOSTS = [
    'localhost', # For local development
    '127.0.0.1', # For local development
    '.render.com', # Allows any subdomain of render.com
    # Add your specific Render service hostname here once deployed, e.g.:
    # 'your-backend-service-name.onrender.com',
    # And any custom domains you might add later:
    # 'api.yourdomain.com',
]
if DEBUG:
    ALLOWED_HOSTS += ['*'] # Allow all hosts in debug mode for easier local testing

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'students',
    'whitenoise.runserver_nostatic', # Add WhiteNoise for serving static files in production
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sms_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sms_backend.wsgi.application'
ASGI_APPLICATION = 'sms_backend.asgi.application'

# Database configuration for PostgreSQL on Render
# Render automatically sets DATABASE_URL for PostgreSQL databases.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'), # Fallback for local development
        conn_max_age=600,
        # Ensure that the DATABASE_URL environment variable is picked up correctly
        # from Render's PostgreSQL service.
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Configure for WhiteNoise to serve static files in production
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Collect static files here

# WhiteNoise storage for compressed and cached static files
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# CORS settings for your GitHub Pages frontend
CORS_ALLOW_ALL_ORIGINS = False # Set to False for production for better security
CORS_ALLOWED_ORIGINS = [
    "https://zxninja.github.io", # Your GitHub Pages frontend URL
    # Add other allowed origins if you have them, e.g., for local frontend dev:
    # "http://localhost:3000",
]

# CSRF_TRUSTED_ORIGINS is crucial for allowing POST requests from your frontend
# Your GitHub Pages URL needs to be here.
CSRF_TRUSTED_ORIGINS = [
    "https://zxninja.github.io",
    # Add your Render backend domain here if you set a custom domain and access it directly
    # "https://your-backend-service-name.onrender.com",
    # "https://api.yourdomain.com",
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Adjust permissions as needed for authentication
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
