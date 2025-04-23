from .base import *  # noqa
import os

# Override the default SECRET_KEY with a required environment variable in production
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required in production!")

###################################################################
# General
###################################################################

DEBUG = False

ALLOWED_HOSTS = ['*']  # You should replace this with your Render domain

###################################################################
# Django security
###################################################################

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    os.environ.get('RENDER_EXTERNAL_URL', 'https://your-app-name.onrender.com')
]

###################################################################
# Static files
###################################################################
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

###################################################################
# Database
###################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DATABASE'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

###################################################################
# CORS
###################################################################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]


