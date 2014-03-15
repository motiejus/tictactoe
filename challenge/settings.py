import os
from challenge.config import config
from django.core.urlresolvers import reverse_lazy

APP_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(APP_DIR)

DEBUG = config.getboolean('challenge', 'debug')

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = config.get('challenge', 'secret_key', fallback='supersecret')

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
    'challenge.tools',
    'challenge.contest',
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

TEMPLATE_DIRS = (
    os.path.join(APP_DIR, 'templates'),
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

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = '/'

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
            }
        }
    }

# Maximum size of Lua code submission
MAX_CODE_SIZE = 60000

# Celery

CELERY_ACCEPT_CONTENT = ['msgpack', 'yaml']
BROKER_URL = 'redis://'
