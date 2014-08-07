# pylint: disable=W0614
import sys
from base import *

#TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    #'--failed',  # Run tests that failed in the last run.
    #'--stop',    # Stop at first failure.
    '--detailed-errors',
    '--verbosity=2',
    '--nocapture',
    # '--pdb',
    '--nologcapture'
    #'--exclude=regex of what you want to exclude',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quest_db', 'USER': 'quest_acct', 'PASSWORD': '12345',
        'HOST': 'localhost', 'PORT': '5432'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s [%(name)s:%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'quest.log',
            'formatter': 'verbose'
        },
       'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers':['console', 'file'],
            'propagate': True,
            'level':'INFO',
        },
        'questapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    }
}