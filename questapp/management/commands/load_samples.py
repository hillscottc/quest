from django.core.management.base import BaseCommand
from questapp.utils import load_samples


class Command(BaseCommand):
    args = '<num>'
    help = 'Parse and load the html files. Defaults to all.'

    def handle(self, *args, **options):
        num = args[0] if args else None
        load_samples(num)

# class Command(NoArgsCommand):
#     help = 'Parese and load all the html files.'
#
#     def handle_noargs(self, **options):
#         load_samples()