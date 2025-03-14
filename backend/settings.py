"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = config('ENVIRONMENT', default='production')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)*b$bj+5s$@bo4%5^f77zd_=(2btl48nr8=@fugxnkvp4rvyno'

DEBUG = ENVIRONMENT == 'local'

if ENVIRONMENT == 'local':
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    ALLOWED_HOSTS = ['podgen-qdyx.onrender.com']

# Media files configuration
MEDIA_URL = '/media/'  # URL path for media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
os.makedirs(MEDIA_ROOT, exist_ok=True)

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
    'backend'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760 # set la taille maximal des fichiers à 10MB

# Logging configuration
os.makedirs(os.path.join(BASE_DIR, 'backend', 'logs'), exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,  # disable Django's default loggers
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Console handler for local development
        'console': {
            'level': 'DEBUG',  # Log all levels during development
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',  # Use the verbose formatter
        },
        # File handler for logs on the server
        'file': {
            'level': 'DEBUG',  # Log all levels to the file
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'backend', 'logs', 'app.log'),  # Save logs to a file
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # Root logger for application-specific logs
        '': {
            'handlers': ['file'] if ENVIRONMENT == 'local' else ['console'],  # Log to file locally, console on Render
            'level': 'DEBUG',  # Capture DEBUG and higher logs
            'propagate': False,
        },
        # Django's logger to suppress excessive logs
        'django': {
            'handlers': ['file'] if ENVIRONMENT == 'local' else ['console'],
            'level': 'WARNING',  # Only show warnings and errors
            'propagate': False,
        },
    },
}

# CORS configuration
if ENVIRONMENT == 'local':
    CORS_ALLOWED_ORIGINS = [
        'http://127.0.0.1',
        'http://localhost',
        "http://localhost:3000",  # React local development server
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://podgen-three.vercel.app",  # accept lien de l'origine du frontend
    ]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'backend.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if ENVIRONMENT == 'local':
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
