# pylint: disable=W0614
from base import *

#TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    #'--failed',  # Run tests that failed in the last run.
    #'--stop',    # Stop at first failure.
    '--detailed-errors',
    '--verbosity=2',
    #'--with-progressive',
    '--nocapture',
    # '--pdb',
    '--nologcapture'
    #'--exclude=regex of what you want to exclude',
]