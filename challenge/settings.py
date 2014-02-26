import os
from challenge.config import config

APP_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(APP_DIR)

DEBUG = config.getboolean('challenge', 'debug')

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = config.get('challenge', 'secret_key', fallback='supersecret')

if not DEBUG:
    assert SECRET_KEY != 'supersecret'

ALLOWED_HOSTS = ['localhost']

DEV_APPS = (
    'django_extensions',
    'debug_toolbar'
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
) + (DEBUG and DEV_APPS or ())

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'challenge.tools.context_processors.debug',
)

ROOT_URLCONF = 'challenge.urls'

WSGI_APPLICATION = 'challenge.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config.get('db', 'engine'),
        'NAME': config.get('db', 'name'),
        'USER': config.get('db', 'user'),
        'PASSWORD': config.get('db', 'password'),
    }
}

# Getting international

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files

STATIC_URL = '/static/'

STATICFILES_STORAGE = ('django.contrib.staticfiles.'
                       'storage.CachedStaticFilesStorage')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
