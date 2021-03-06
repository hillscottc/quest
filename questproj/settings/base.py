import os
PROJ_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '99%rg_8lh6wyegbj$f+0l%_+j%!_rggp#iveieaz%#b0i@ix8c'

SITE_ID = 1

## Djangp TestCases force DEBUG=False, ignoring the settings file.
## Can override with @override_settings(DEBUG=True). To see django.db logging, for example.
DEBUG = True
TEMPLATE_DEBUG = True

# Allow all host headers
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'django.contrib.humanize',  # http://stackoverflow.com/questions/346467/format-numbers-in-django-templates
    # 'django_stormpath',
    # 'registration',
    'questapp',
)

# AUTHENTICATION_BACKENDS = (
#     'django_stormpath.backends.StormpathIdSiteBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )
#
# AUTH_USER_MODEL = 'django_stormpath.StormpathUser'
#
# STORMPATH_ID = os.environ.get('STORMPATH_API_KEY_ID')
# STORMPATH_SECRET = os.environ.get('STORMPATH_API_KEY_SECRET')
# STORMPATH_APPLICATION = os.environ.get('STORMPATH_URL')
# STORMPATH_ID_SITE_CALLBACK_URI = 'http://trivquest.com/stormpath-id-site-callback/'
# LOGIN_REDIRECT_URL = '/'  # After successful log in


# API_LIMIT_PER_PAGE = 500     # Default num of recs tastypie will return.

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

ROOT_URLCONF = 'questproj.urls'
WSGI_APPLICATION = 'questproj.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(PROJ_DIR, "templates"),
    os.path.join(os.path.dirname(PROJ_DIR), 'questapp', "templates"),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = 'staticfiles'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(PROJ_DIR, "static"), )

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


LOGS_DIR = os.path.join(os.path.dirname(BASE_DIR),  'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {'format': '%(levelname)s [%(name)s:%(lineno)s] %(message)s'},
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
        'quest_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'quest.log'),
            'formatter': 'verbose'
        },
        'django_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'quest_log'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'django_log'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['console', 'django_log'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'quest_log'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# The ON_HEROKU variable is defind heroku app env, with heroku:config.
# It will only be true when running the app in Heroku.
ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {'simple': {'format': '%(levelname)s [%(name)s:%(lineno)s] %(message)s'}},
        'filters': {},
        'handlers': {
            'null': {'level': 'DEBUG', 'class': 'logging.NullHandler'},
            'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'simple'}
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG'}
        }
    }

else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                             'NAME': 'quest_db', 'USER': 'quest_acct', 'PASSWORD': '12345',
                             'HOST': 'localhost', 'PORT': '5432'}}

SITE_NAME = "TrivQuest"

# REGISTRATION_OPEN = True
# ACCOUNT_ACTIVATION_DAYS = 14
# REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
# LOGIN_URL = '/accounts/login/'  # Where users go if not logged in and try to access a page requiring auth

# EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
# POSTMARK_API_KEY = os.environ['POSTMARK_API_KEY']
# POSTMARK_SENDER = 'scott@trivquest.com'

