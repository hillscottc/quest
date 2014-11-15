from base import *
import os


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    #'--failed',  # Run tests that failed in the last run.
    #'--stop',    # Stop at first failure.
    '--detailed-errors',
    '--verbosity=2',
    '--nocapture',
    # '--pdb',
    '--nologcapture',
    # '--with-fixture-bundling'
]

# define if on heroku environment
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

else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                             'NAME': 'quest_db', 'USER': 'quest_acct', 'PASSWORD': '12345',
                             'HOST': 'localhost', 'PORT': '5432'}}
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}







