import os
PROJ_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '99%rg_8lh6wyegbj$f+0l%_+j%!_rggp#iveieaz%#b0i@ix8c'

## Djangp TestCases force DEBUG=False, ignoring the settings file.
## Can override with @override_settings(DEBUG=True). To see django.db logging, for example.
DEBUG = True
TEMPLATE_DEBUG = True

# Allow all host headers
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'bootstrap3',
    'questapp',
    'quizapp',
)

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
    'questapp.context_processors.base_context',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

ROOT_URLCONF = 'questproj.urls'
WSGI_APPLICATION = 'questproj.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJ_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


TEMPLATE_DIRS = (
    os.path.join(PROJ_DIR, "templates"),
    os.path.join('questapp', "templates"),
    os.path.join('quizapp', "templates"),
)

SITE_NAME = "Question Site"

QUIZ_SCRAPE_DIR = os.path.join(os.path.dirname(PROJ_DIR), 'html_data_sources', 'quizballs')
JEAP_SRC_DIR = os.path.join(os.path.dirname(PROJ_DIR), 'html_data_sources', 'jeap')
JEAP_ID_FILE = os.path.join(os.path.dirname(PROJ_DIR), 'html_data_sources', 'jeap_src_ids.txt')

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = 'staticfiles'
STATIC_ROOT= os.path.join(os.path.dirname(BASE_DIR),'staticfiles')

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(PROJ_DIR, "static"), )


LOGS_DIR = os.path.join(os.path.dirname(BASE_DIR),  'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s [%(name)s:%(lineno)s] %(message)s'

        },
    },
    'filters': {},
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 'quest_log': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(LOGS_DIR, 'quest.log'),
        #     'formatter': 'verbose'
        # },
        # 'django_log': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(LOGS_DIR, 'django.log'),
        #     'formatter': 'verbose'
        # },
    },
    'loggers': {
        '': {
            # 'handlers': ['console', 'quest_log'],
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        # 'django': {
        #     'handlers': ['console', 'django_log'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
        # 'django.db.backends': {
        #     'handlers': ['console', 'django_log'],
        #     'propagate': True,
        #     'level': 'INFO',
        # },
        # 'django.request': {
        #     'handlers': ['console', 'quest_log'],
        #     'level': 'ERROR',
        #     'propagate': True,
        # },
    }
}
