import re
from project.base_settings import *

DEBUG = False

# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_COOKIE_AGE = 15 * 60
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_IDLE_TIMEOUT = 15
# info: http://stackoverflow.com/questions/14830669/how-to-expire-django-session-in-5minutes

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-cache-name',
#     }
# }

# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
# ]

LOG_LEVEL = 'WARNING'
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
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': LOG_DIR + 'typers.log',
        },
        'mail_admins': {
            'level': LOG_LEVEL,
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        '': {
            'level': LOG_LEVEL,
            'handlers': ['file'],
            'propagate': False,
        },
        'django': {
            'level': LOG_LEVEL,
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        'requests': {
            'level': LOG_LEVEL,
            'handlers': ['mail_admins'],
            'propagate': True,
        },
    },
}

ADMINS = (
    ('Dawid Figiel', 'dawid.figiel@gmail.com'),
)
MANAGERS = ADMINS

APPEND_SLASH = False

IGNORABLE_404_URLS = (
    re.compile(r'^/.*\.(php|cgi|do|action|asmx|asp|txt|ico)/?$'),
    re.compile(r'^/php.*'),
    re.compile(r'^/2php.*'),
    re.compile(r'^/sql.*'),
    re.compile(r'^/mysql.*'),
    re.compile(r'^/pma.*'),
    re.compile(r'^/PMA.*'),
    re.compile(r'^/db.*'),
    re.compile(r'^/myadmin.*'),
    re.compile(r'^/proxy.*'),
    re.compile(r'^/program.*'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
)
