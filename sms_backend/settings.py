# sms_backend/settings.py
# This file contains the main configuration for your Django project.

import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'slm$kz=tkjmztcjtke&vqh0-4)-@=$k57#oeaq@^r5sui)e%wa')

# Set DEBUG to False for production.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Allowed hosts for your Django application.
# Use an environment variable for production hosts.
# For local development, '127.0.0.1' and 'localhost' are always implicitly allowed by Django if DEBUG is True.
# When DEBUG is False, you MUST explicitly list allowed hosts.
# We will use an environment variable for this.
# The split(',') ensures that if you put "host1,host2" in the env var, it becomes a list.
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Only apply specific hosts if DEBUG is False and ALLOWED_HOSTS from env is empty,
# or if you want to override for local dev with specific hosts.
# A simpler approach is to rely *solely* on the environment variable for production.
# The primary reason for the 400 error is that when DEBUG is False, the 'if DEBUG:' block is skipped,
# and if DJANGO_ALLOWED_HOSTS isn't set, ALLOWED_HOSTS becomes an empty list, causing the 400 error.
# The best fix is to ensure DJANGO_ALLOWED_HOSTS env var is ALWAYS set correctly on Render.
# The code below *correctly* handles the case where the env var might be empty.


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
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'Frontend',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://zxninja.github.io",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
