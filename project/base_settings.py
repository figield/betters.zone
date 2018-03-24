import os
import netifaces

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAX_TOURNAMENTS = 10
MAX_ROUNDS = 20
MAX_MATCHES = 20
IS_STAFF = True

USER_CACHE_TIMEOUT = 10
INDEX_CACHE_TIMEOUT = 30
SHORT_INDEX_CACHE_TIMEOUT = 10

MAX_UPLOAD_SIZE = 43008  # 43008 - 42 KB, 2621440 - 2,5 MB

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'typers',
    'quiz'
]

SITE_ID = 1

ACCOUNT_ACTIVATION_DAYS = 7

MIDDLEWARE = [
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates/registration'),
                 os.path.join(BASE_DIR, 'templates/typers'),
                 os.path.join(BASE_DIR, 'templates/typers/friends'),
                 os.path.join(BASE_DIR, 'templates/typers/rankings'),
                 os.path.join(BASE_DIR, 'templates/typers/teams'),
                 os.path.join(BASE_DIR, 'templates/typers/tournaments')
                 ],
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

WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'  # 'UTC'

USE_I18N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), os.path.join(BASE_DIR, "frontend_quizvote")]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = "TypersLeague"

SEND_BROKEN_LINK_EMAILS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'typersleague',
        'USER': 'typersleague',
        'PASSWORD': 'typersleague',
        'HOST': '127.0.0.1',
        'PORT': '',  # '5432',
    }
}


# Find out what the IP addresses are at run time
# This is necessary because otherwise Gunicorn will reject the connections
def ip_addresses():
    ip_list = ['localhost']
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        for x in (netifaces.AF_INET, netifaces.AF_INET6):
            if x in addrs:
                ip_list.append(addrs[x][0]['addr'])
    return ip_list


# Discover our IP address
ALLOWED_HOSTS = ip_addresses()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# TODO: note sure if needed for angular
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TOOLBAR = False
