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
