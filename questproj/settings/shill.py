from base import *
import os


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--detailed-errors', '--verbosity=2',
    '--nocapture', '--nologcapture',
    #'--failed',  # Run tests that failed in the last run.
    #'--stop',    # Stop at first failure.
    # '--pdb',
]

# The ON_HEROKU variable is defind heroku app env, with heroku:config.
# It will only be true when running the app in Heroku.
ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
    CACHES = {'default': {'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                          'TIMEOUT': 500, 'BINARY': True,
                          'OPTIONS': { 'tcp_nodelay': True }}}

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
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}







