"""
Parses the samples html files and loads them to db.
"""
import logging
from questapp.game_mgr import load_all_games
from questapp.models import Clue, Game
from django.core.management.base import BaseCommand

log = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Parses the samples html files and loads them to db.'

    def handle(self, *args, **options):
        load_all_games()
        log.info("Loaded samples. {} games, {} clues.".format(
            Game.objects.count(), Clue.objects.count()))

