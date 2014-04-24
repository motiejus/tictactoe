import os
from tictactoe.config import config
from django.core.urlresolvers import reverse_lazy

APP_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(APP_DIR)

DEBUG = config.getboolean('tictactoe', 'debug')

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = config.get('tictactoe', 'secret_key', fallback='supersecret')

ALLOWED_HOSTS = ['tictactoe.spilgames.com']

ADMINS = (('Motiejus', 'motiejus.jakstys@spilgames.com'),)
MANAGERS = ADMINS

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

    'jquery',
    'bootstrap',

    'tictactoe.tools',
    'tictactoe.contest',
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
    'tictactoe.tools.context_processors.debug',
)

TEMPLATE_DIRS = (
    os.path.join(APP_DIR, 'templates'),
)

ROOT_URLCONF = 'tictactoe.urls'

WSGI_APPLICATION = 'tictactoe.wsgi.application'

_DBNAME, _DBENGINE = config.get('db', 'name'), config.get('db', 'engine')
if DEBUG and "sqlite" in _DBENGINE and "/" not in _DBNAME:
    _DBNAME = os.path.join(BASE_DIR, _DBNAME)

DATABASES = {
    'default': {
        'ENGINE': _DBENGINE,
        'NAME': _DBNAME,
        'USER': config.get('db', 'user'),
        'PASSWORD': config.get('db', 'password'),
        'HOST': config.get('db', 'host'),
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

STATICFILES_DIRS = (os.path.join(APP_DIR, 'static'),)

STATIC_ROOT = config.get('tictactoe', 'static_root') or \
    os.path.join(BASE_DIR, 'static')

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = '/'

TOTAL_CAPS = config.getint('tictactoe', 'total_caps')

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'timed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
        'syslog': {
            'level': 'DEBUG',
            'class': 'logbook.compat.RedirectLoggingHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'tictactoe': {
            'handlers': ['console', 'syslog'],
            'propagate': True,
            'level': 'INFO',
            },
        'django': {
            'handlers': ['console', 'syslog'],
            'propagate': True,
            'level': 'INFO',
            }
        }
    }

# Maximum size of Lua code submission
MAX_CODE_SIZE = 60000

# Celery

CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_ACCEPT_CONTENT = ['msgpack', 'yaml']
BROKER_URL = 'redis://'

FIGHT_CGROUP = config.get('limits', 'cgroup')
_FIGHT_MEMORY_LIMIT = config.get('limits', 'memory')
FIGHT_MEMORY_LIMIT = _FIGHT_MEMORY_LIMIT and int(_FIGHT_MEMORY_LIMIT) or None
FIGHT_TIMEOUT = config.getfloat('limits', 'timeout')


import logbook
import logbook.handlers

# add syslog handler
syslog_handler = logbook.handlers.SyslogHandler(
    application_name='tictactoe', facility='local6',
    address=('localhost', 514)
    )
syslog_handler.push_application()
