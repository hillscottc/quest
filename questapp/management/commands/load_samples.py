"""
Parses the samples html files and loads them to db.
"""
from questapp.jeap_src_utils import load_samples
from questapp.models import get_relevant_counts
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Parses the samples html files and loads them to db.'

    def handle(self, *args, **options):

        load_samples()
        print get_relevant_counts()

