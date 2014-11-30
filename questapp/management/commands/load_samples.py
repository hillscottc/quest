from django.core.management.base import NoArgsCommand
from questapp.utils import load_samples

class Command(NoArgsCommand):
    help = 'Parese and load all the html files.'

    def handle_noargs(self, **options):
        load_samples()