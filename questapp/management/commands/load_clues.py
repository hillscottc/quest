from django.core.management.base import BaseCommand
from questapp.utils import load_clues


class Command(BaseCommand):
    args = '<infile>'
    help = 'Loads a json dump file of Clues.'

    def handle(self, *args, **options):
        if not args:
            raise ValueError("Input file arg not specified.")
        load_clues(args[0])

