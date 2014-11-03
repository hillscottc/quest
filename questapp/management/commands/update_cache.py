from django.core.management.base import NoArgsCommand
from django.core.cache import cache
from questapp.models import Clue
from questproj.utils import get_random_objs


class Command(NoArgsCommand):
    help = 'Refreshes my cache.'

    def handle_noargs(self, **options):
        qs = list(get_random_objs(Clue, 1000))
        cache.set('random-clues', qs)