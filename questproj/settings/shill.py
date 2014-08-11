from base import *

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quest_db', 'USER': 'quest_acct', 'PASSWORD': '12345',
        'HOST': 'localhost', 'PORT': '5432'
    }
}

LOGS_DIR = os.path.join(os.path.dirname(PROJ_DIR), 'logs')
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
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'quest': {
            'handlers': ['console', 'quest_log'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}



