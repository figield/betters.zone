from project.base_settings import *
from pathlib import Path

DEBUG = True

# http://django-debug-toolbar.readthedocs.io/en/stable/installation.html
debug_file = Path(BASE_DIR + '/debug_toolbar')
if debug_file.is_file():
    TOOLBAR = True
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

INTERNAL_IPS = ['127.0.0.1']  # debug_toolbar

LOG_LEVEL = 'DEBUG'
LOG_DIR = '/tmp/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'django': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'requests': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False
        },
    },
}
