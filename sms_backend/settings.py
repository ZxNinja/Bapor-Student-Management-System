# sms_backend/settings.py
# This file contains the main configuration for your Django project.

import os
import dj_database_url # Used for parsing database URLs from environment variables
from pathlib import Path # Python 3.4+ standard library for filesystem paths

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable for production SECRET_KEY for security.
# Provide a dummy key for local development.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'slm$kz=tkjmztcjtke&vqh0-4)-@=$k57#oeaq@^r5sui)e%wa')


# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG to False for production.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Allowed hosts for your Django application.
# In production, this should include your backend's domain (e.g., Render domain)
# and potentially '127.0.0.1' for health checks.
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
# If DEBUG is True, allow all for convenience (be careful in production)
if DEBUG:
    ALLOWED_HOSTS = ['.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework', # Django REST Framework for building APIs
    'corsheaders',    # For handling Cross-Origin Resource Sharing
    # Your project apps
    'students',       # Your student management application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Must be placed high up
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
        # DIRS now points to the project's base directory, allowing index.html to be found.
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Use dj-database-url to parse the DATABASE_URL environment variable.
# This is common for production environments like Render, Heroku, etc.
# Fallback to SQLite for local development if DATABASE_URL is not set.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600 # Optional: connection lifespan for persistent connections
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) configuration
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/' # The URL prefix for static files.
# This tells Django where to find your static files (css, js) during development
STATICFILES_DIRS = [
    BASE_DIR / 'Frontend', # Assuming your frontend static files are here
]

# The directory where `collectstatic` will gather all static files for production serving.
# This should be outside your project root, or handled by your hosting provider.
STATIC_ROOT = BASE_DIR / 'staticfiles'


# CORS configuration for your frontend API calls
# In production, specify your frontend's exact URL (e.g., your GitHub Pages URL).
CORS_ALLOW_ALL_ORIGINS = False # IMPORTANT: Set to False for production!
CORS_ALLOWED_ORIGINS = [
    "https://zxninja.github.io", # Your GitHub Pages frontend URL
    # Add other domains if necessary (e.g., localhost for local frontend dev)
]
# If you need to allow credentials (e.g., cookies, authorization headers)
# CORS_ALLOW_CREDENTIALS = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings (optional, but good practice)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Allows unauthenticated access to API (for simplicity)
        # In a real app, you might use: 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
