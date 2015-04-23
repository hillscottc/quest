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

# STORMPATH_ID_SITE_CALLBACK_URI = 'http://localhost:8000/stormpath-id-site-callback/'
