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




