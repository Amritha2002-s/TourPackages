import os
from pathlib import Path

# ✅ Define BASE_DIR at the top
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = 'your-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tour',  # Our app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tour_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'tour_management.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tour1',  # Change to your database name
        'USER': 'root',  # Default user in XAMPP
        'PASSWORD': '',  # XAMPP default has no password
        'HOST': '127.0.0.1',  # Localhost
        'PORT': '3306',  # Default MySQL port
        'OPTIONS': {
        }
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

LOGIN_URL = 'login'
AUTH_USER_MODEL = 'tour.CustomUser'


RAZORPAY_KEY_ID = "rzp_test_HwZtmbbTnuY8XE"
RAZORPAY_KEY_SECRET = "7nOgvir4kX0peYcspa6nzsUl"