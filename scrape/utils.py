"""Gets html pages from Quizballs, saves to local dir.
"""
import os
from django.conf import settings

## For saving files...
FILE_BASE_DIR = os.path.join(settings.PROJ_DIR, 'scrape', 'files', 'quizballs')
FILENAME_TEMPLATE = "{}.html"


